# Resume Parser Test Fixtures

Place sample resume files here for unit + integration tests.
At minimum include one of each type:

| File | Type | What it tests |
|---|---|---|
| `single_column_good.pdf` | Machine-generated PDF, single column | Happy path parsing |
| `canva_two_column.pdf` | Canva-style two-column template | Multi-column ATS flag |
| `scanned_image.pdf` | Scanned/image-only | No-text fallback warning |
| `standard_resume.docx` | Well-formed DOCX | DOCX happy path |
| `table_skills.docx` | DOCX with table-based skills section | Table detection warning |

Do NOT commit real student resumes. Use synthetic / anonymised data only.
