import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

BLOCKED_TEXT_PATTERNS = [
    "captcha",
    "verify you are human",
    "otp",
    "one time password",
    "sign in",
    "login",
    "log in",
]


class PlaywrightAutoApplySession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def open(self, url: str) -> str:
        try:
            self.playwright = await async_playwright().start()

            self.browser = await self.playwright.chromium.launch(
                headless=False,
                slow_mo=150,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                ],
            )

            self.context = await self.browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )

            self.page = await self.context.new_page()
            self.page.set_default_timeout(8000)

            try:
                await self.page.goto(url, wait_until="domcontentloaded", timeout=25000)
            except PlaywrightTimeoutError:
                logger.warning("Page load timeout. Continuing with current page state.")

            await self.page.wait_for_timeout(2500)
            return self.page.url

        except Exception as exc:
            logger.exception("Browser open failed for URL: %s", url)
            await self.close()
            raise RuntimeError(f"Browser open failed: {exc}")

    async def close(self) -> None:
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as exc:
            logger.warning("Failed to close browser session: %s", exc)

    async def detect_blockers(self) -> Optional[str]:
        try:
            content = (await self.page.content()).lower()
        except Exception:
            return None

        for pattern in BLOCKED_TEXT_PATTERNS:
            if pattern in content:
                return f"Blocked because page appears to require {pattern}."

        return None

    async def inspect_fields(self) -> List[Dict[str, Any]]:
        fields = []

        try:
            locators = self.page.locator("input, textarea, select")
            count = await locators.count()
        except Exception:
            return fields

        for index in range(count):
            element = locators.nth(index)

            try:
                tag = await element.evaluate("el => el.tagName.toLowerCase()")
                input_type = await element.get_attribute("type") or ""
                name = await element.get_attribute("name") or ""
                field_id = await element.get_attribute("id") or ""
                placeholder = await element.get_attribute("placeholder") or ""
                aria_label = await element.get_attribute("aria-label") or ""

                fields.append(
                    {
                        "index": index,
                        "tag": tag,
                        "type": input_type,
                        "name": name,
                        "id": field_id,
                        "placeholder": placeholder,
                        "aria_label": aria_label,
                    }
                )
            except Exception:
                continue

        return fields

    def _field_text(self, field: Dict[str, Any]) -> str:
        return " ".join(
            [
                field.get("name", ""),
                field.get("id", ""),
                field.get("placeholder", ""),
                field.get("aria_label", ""),
                field.get("type", ""),
            ]
        ).lower()

    def _value_for_field(self, field_text: str, candidate: Dict[str, Any]) -> Optional[str]:
        mapping = [
            (["full name", "fullname", "name"], candidate.get("full_name")),
            (["email", "e-mail"], candidate.get("email")),
            (["phone", "mobile", "contact"], candidate.get("phone")),
            (["location", "city", "current location"], candidate.get("current_location")),
            (["linkedin"], candidate.get("linkedin_url")),
            (["github"], candidate.get("github_url")),
            (["portfolio", "website"], candidate.get("portfolio_url")),
            (["salary", "ctc", "expected"], candidate.get("expected_salary")),
            (["notice"], candidate.get("notice_period")),
            (["relocate", "relocation"], candidate.get("willing_to_relocate")),
            (["authorization", "work permit"], candidate.get("work_authorization")),
            (["cover letter", "message", "why"], candidate.get("cover_letter")),
        ]

        for keywords, value in mapping:
            if value and any(keyword in field_text for keyword in keywords):
                return value

        return None

    async def fill_fields(self, candidate: Dict[str, Any]) -> List[Dict[str, Any]]:
        filled = []

        try:
            locators = self.page.locator("input, textarea")
            count = await locators.count()
        except Exception:
            return filled

        for index in range(count):
            element = locators.nth(index)

            try:
                if not await element.is_visible():
                    continue

                input_type = (await element.get_attribute("type") or "").lower()

                if input_type in {"hidden", "submit", "button", "checkbox", "radio", "file"}:
                    continue

                field = {
                    "name": await element.get_attribute("name") or "",
                    "id": await element.get_attribute("id") or "",
                    "placeholder": await element.get_attribute("placeholder") or "",
                    "aria_label": await element.get_attribute("aria-label") or "",
                    "type": input_type,
                }

                field_text = self._field_text(field)
                value = self._value_for_field(field_text, candidate)

                if not value:
                    continue

                await element.fill(str(value), timeout=5000)
                filled.append({"field": field_text, "value": value})

            except Exception:
                continue

        return filled

    async def upload_resume(self, resume_path: str) -> bool:
        path = Path(resume_path)

        if not path.exists():
            return False

        try:
            file_inputs = self.page.locator("input[type='file']")
            count = await file_inputs.count()

            if count == 0:
                return False

            await file_inputs.first.set_input_files(str(path))
            return True

        except Exception as exc:
            logger.warning("Resume upload failed: %s", exc)
            return False

    async def submit_application(self) -> bool:
        if not self.page:
            return False

        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "[role='button']:has-text('Submit')",
            "[role='button']:has-text('Apply')",
            "[role='button']:has-text('Continue')",
            "[role='button']:has-text('Next')",
            "button:has-text('Submit')",
            "button:has-text('Submit application')",
            "button:has-text('Send application')",
            "button:has-text('Apply')",
            "button:has-text('Apply now')",
            "button:has-text('Continue')",
            "button:has-text('Next')",
            "button:has-text('Review')",
            "button:has-text('Review application')",
            "button:has-text('Save and continue')",
            "input[value='Submit']",
            "input[value='Apply']",
            "input[value='Continue']",
            "input[value='Next']",
        ]

        for selector in submit_selectors:
            try:
                locator = self.page.locator(selector)
                count = await locator.count()

                for index in range(count):
                    button = locator.nth(index)

                    if await button.is_visible() and await button.is_enabled():
                        await button.scroll_into_view_if_needed(timeout=3000)
                        await button.click(timeout=8000)
                        await self.page.wait_for_timeout(2500)
                        return True

            except Exception:
                continue

        return False