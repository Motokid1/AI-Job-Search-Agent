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
