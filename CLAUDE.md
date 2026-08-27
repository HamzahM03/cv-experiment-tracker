# CLAUDE.md

## Architecture

- Entities are organized as `router → service → repository → schema` layers: routers handle HTTP concerns and translate not-found results into `HTTPException(404)`, services hold business/orchestration logic (including cross-entity checks like nested-resource ownership), and repositories are where `Session`/`select`/`db.commit()` calls happen. When adding to an existing entity, follow the layer where similar logic already lives rather than introducing a shortcut that bypasses it.
- Cross-entity ownership checks (e.g. "does this dataset belong to this project") are currently done in the service layer. This doesn't preclude also adding DB-level constraints where appropriate — it just reflects where that logic lives today.
- Repository functions generally take unpacked primitives (`name`, `description`, ...) rather than schema objects — services unpack Pydantic models into kwargs before calling the repo.
- `None` returned from a service typically signals "not found"; routers convert that into a 404.
- Repository write functions currently follow `db.commit()` + `db.refresh()` before returning the object — a pattern to be consistent with, not a fixed rule if a case calls for different transaction handling.
- Schemas per entity generally follow `...Create`, `...Update` (optional fields, applied via `model_dump(exclude_unset=True)`), `...Response` (`ConfigDict(from_attributes=True)`).
- HTML routes return `Jinja2Templates.TemplateResponse` rather than a `response_model`; templates are organized into `pages/` (full pages), `partials/` (HTMX swap targets), and `components/` (reusable fragments).
- `.env` + `python-dotenv` supplies `DATABASE_URL`, read in both `app/db/database.py` and `alembic/env.py`.

## General

- Prefer small, focused changes scoped to the task at hand. Avoid unrelated refactors, renames, or cleanup in the same change unless asked.
