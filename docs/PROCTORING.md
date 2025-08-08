# Proctoring Integration (Robeli)

This project integrates the edx-proctoring subsystem to support timed and proctored exams. Key changes:

- Enabled special exams and proctoring by default in both LMS and Studio
- New subsections (sequentials) created in Studio default to Proctored Timed Exams (authors can change/remove)
- Platform branding updated to use "Robeli" in user-facing strings
- Proctoring backends configured with a default mock backend
- Proctoring library is sourced from the user's fork: https://github.com/Tshiamo-ctrl/edx-proctoring

## Defaults and Behavior

- When creating a new Subsection in Studio, if the course has proctoring enabled and special exams are enabled, the Subsection is created with:
  - `is_time_limited = True`
  - `is_proctored_enabled = True`
  - `hide_after_due = True`
- Authors can edit the Subsection and switch the exam type to None, Timed, Proctored, Practice Proctored, or Onboarding as usual.

## Monitoring/Instructor Dashboard

- The Instructor Dashboard Special Exams tab remains available and uses edx-proctoring APIs for:
  - Allowances
  - Onboarding
  - Attempts and results report (CSV)
- If configured with LTI based proctoring (`lti_external`), the Exams dashboard MFE link will be shown when the setting `EXAMS_DASHBOARD_MICROFRONTEND_URL` is provided.

## Configuration

- LMS settings (`lms/envs/common.py`):
  - `FEATURES['ENABLE_SPECIAL_EXAMS'] = True`
  - `FEATURES['ENABLE_PROCTORED_EXAMS'] = True`
  - `PROCTORING_BACKENDS = { 'DEFAULT': 'mock', 'mock': {}, 'mock_proctoring_without_rules': {}, 'lti_external': {} }`
  - `PLATFORM_NAME = 'Robeli'`
- CMS settings (`cms/envs/common.py`):
  - `FEATURES['ENABLE_SPECIAL_EXAMS'] = True`
  - `FEATURES['ENABLE_PROCTORED_EXAMS'] = True`
  - `PROCTORING_BACKENDS = { 'DEFAULT': 'mock', 'mock': {}, 'mock_proctoring_without_rules': {}, 'lti_external': {} }`
  - `PLATFORM_NAME = 'Robeli'`

## Dependency

- requirements/github.in now includes:
  - `git+https://github.com/Tshiamo-ctrl/edx-proctoring.git@master#egg=edx-proctoring==0.0`
- Compiled requirement files pin `edx-proctoring==0.0` to pick up the VCS dependency (updated in:
  - `requirements/edx/base.txt`
  - `requirements/edx/development.txt`
  - `requirements/edx/testing.txt`
  - `requirements/edx/doc.txt`
)

## Code Changes

- `cms/djangoapps/contentstore/xblock_storage_handlers/create_xblock.py`:
  - Added default fields when creating a new `sequential` to make it a proctored timed exam when enabled.
- Branding:
  - `PLATFORM_NAME` set to `Robeli` in LMS and CMS common settings.

## Rollback/Opt-out

- To disable default proctoring on creation, set either:
  - `FEATURES['ENABLE_SPECIAL_EXAMS'] = False` (LMS and CMS), or
  - Disable proctoring at the course level (`enable_proctored_exams = False`).
- Authors can also manually switch the Subsection exam type to "None" in Studio.

## Notes

- The mock backend is suitable for development/testing. For production, define a real backend configuration in `PROCTORING_BACKENDS`.
- Ensure `EXAMS_DASHBOARD_MICROFRONTEND_URL` is configured if using the separate Exams Dashboard MFE.