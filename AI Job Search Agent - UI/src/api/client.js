const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

async function parseError(response) {
  try {
    const data = await response.json();
    return data.detail || "Request failed.";
  } catch {
    return "Request failed.";
  }
}

export async function searchJobsManual(payload) {
  const response = await fetch(`${API_BASE_URL}/jobs/search/manual`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function extractResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/resume/extract`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function searchJobsResume(formValues) {
  const formData = new FormData();
  formData.append("file", formValues.file);

  if (formValues.packageMinLpa) {
    formData.append("package_min_lpa", formValues.packageMinLpa);
  }
  if (formValues.packageMaxLpa) {
    formData.append("package_max_lpa", formValues.packageMaxLpa);
  }
  if (formValues.location) {
    formData.append("location", formValues.location);
  }
  if (formValues.desiredRole) {
    formData.append("desired_role", formValues.desiredRole);
  }
  if (formValues.companies) {
    formData.append("companies", formValues.companies);
  }

  const response = await fetch(`${API_BASE_URL}/jobs/search/resume`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function analyzeResume(formValues) {
  const formData = new FormData();
  formData.append("file", formValues.file);
  formData.append("target_role", formValues.targetRole);

  if (formValues.packageMinLpa) {
    formData.append("package_min_lpa", formValues.packageMinLpa);
  }
  if (formValues.packageMaxLpa) {
    formData.append("package_max_lpa", formValues.packageMaxLpa);
  }
  if (formValues.location) {
    formData.append("location", formValues.location);
  }
  if (formValues.companies) {
    formData.append("companies", formValues.companies);
  }
  if (formValues.targetDomain) {
    formData.append("target_domain", formValues.targetDomain);
  }

  const response = await fetch(`${API_BASE_URL}/analysis/resume`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function fetchJobDetail(job) {
  const formData = new FormData();
  formData.append("job_payload", JSON.stringify(job));

  const response = await fetch(`${API_BASE_URL}/jobs/detail`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function matchResumeForJob(file, job) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_payload", JSON.stringify(job));

  const response = await fetch(`${API_BASE_URL}/match/job-resume`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function prepareApplicationPackage(file, job, preferences) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_payload", JSON.stringify(job));

  if (preferences.coverLetterTone) {
    formData.append("cover_letter_tone", preferences.coverLetterTone);
  }
  if (preferences.noticePeriod) {
    formData.append("notice_period", preferences.noticePeriod);
  }
  if (preferences.expectedSalary) {
    formData.append("expected_salary", preferences.expectedSalary);
  }
  if (preferences.currentLocation) {
    formData.append("current_location", preferences.currentLocation);
  }
  if (preferences.willingToRelocate) {
    formData.append("willing_to_relocate", preferences.willingToRelocate);
  }
  if (preferences.workAuthorization) {
    formData.append("work_authorization", preferences.workAuthorization);
  }
  if (preferences.portfolioUrl) {
    formData.append("portfolio_url", preferences.portfolioUrl);
  }
  if (preferences.githubUrl) {
    formData.append("github_url", preferences.githubUrl);
  }
  if (preferences.linkedinUrl) {
    formData.append("linkedin_url", preferences.linkedinUrl);
  }

  const response = await fetch(`${API_BASE_URL}/apply/prepare`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function createTrackedApplication(payload) {
  const response = await fetch(`${API_BASE_URL}/tracker/applications`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function getTrackedApplications(params = {}) {
  const query = new URLSearchParams();

  if (params.status && params.status !== "All") {
    query.append("status", params.status);
  }

  if (params.sortBy) {
    query.append("sort_by", params.sortBy);
  }

  if (params.sortOrder) {
    query.append("sort_order", params.sortOrder);
  }

  const url = `${API_BASE_URL}/tracker/applications${
    query.toString() ? `?${query.toString()}` : ""
  }`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function updateTrackedApplication(id, payload) {
  const response = await fetch(`${API_BASE_URL}/tracker/applications/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function deleteTrackedApplication(id) {
  const response = await fetch(`${API_BASE_URL}/tracker/applications/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}
export async function startAutoApplySession(file, job, candidate) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_payload", JSON.stringify(job));
  formData.append("candidate_payload", JSON.stringify(candidate));

  const response = await fetch(`${API_BASE_URL}/auto-apply/start`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function getAutoApplySession(sessionId) {
  const response = await fetch(
    `${API_BASE_URL}/auto-apply/session/${sessionId}`,
  );

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function resumeAutoApplySession(sessionId, decision) {
  const response = await fetch(
    `${API_BASE_URL}/auto-apply/session/${sessionId}/resume`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ decision }),
    },
  );

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function cancelAutoApplySession(sessionId) {
  const response = await fetch(
    `${API_BASE_URL}/auto-apply/session/${sessionId}/cancel`,
    {
      method: "POST",
    },
  );

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}
