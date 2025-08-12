# create_domain.py
# Cambio: ajustado para estructura con main.py en la raíz y db en app/core/db.py

from pathlib import Path
import re

domain = input("Nombre del dominio: ").strip().lower()
if not re.fullmatch(r"[a-z][a-z0-9_]*", domain):
    raise SystemExit("Nombre inválido. Usa minúsculas, números y _; debe empezar por letra.")

Pascal = "".join(p.capitalize() for p in domain.split("_"))

# Cambio: rutas según tu árbol real
project_root = Path(".").resolve()
app_dir = project_root / "app"
domain_dir = app_dir / "domain" / domain
routers_dir = app_dir / "routers"
main_file = project_root / "main.py"

if not main_file.exists():
    raise SystemExit(f"No se encontró main.py en {main_file}")

domain_dir.mkdir(parents=True, exist_ok=True)
routers_dir.mkdir(parents=True, exist_ok=True)

# Cambio: asegurar __init__.py para paquetes
for p in [
    app_dir,
    app_dir / "core",
    app_dir / "domain",
    domain_dir,
    routers_dir,
]:
    initf = p / "__init__.py"
    if not initf.exists():
        initf.write_text("")

models_py = f"""from typing import Optional
from sqlmodel import SQLModel, Field

class {Pascal}(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
"""

repository_py = f"""from sqlmodel import Session, select
from .models import {Pascal}

class {Pascal}Repository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self):
        return self.session.exec(select({Pascal})).all()

    def create(self, obj: {Pascal}):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
"""

service_py = f"""from sqlmodel import Session
from .models import {Pascal}
from .repository import {Pascal}Repository

class {Pascal}Service:
    def __init__(self, session: Session):
        self.repo = {Pascal}Repository(session)

    def list_all(self):
        return self.repo.list_all()

    def create(self, data: dict):
        return self.repo.create({Pascal}(**data))
"""

# Cambio: import correcto de engine desde app/core/db.py y rutas relativas desde routers/
router_py = f"""from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..core.db import engine
from ..domain.{domain}.service import {Pascal}Service

router = APIRouter(prefix="/{domain}", tags=["{domain}"])

def get_session():
    with Session(engine) as s:
        yield s

@router.get("")
def list_{domain}(session: Session = Depends(get_session)):
    svc = {Pascal}Service(session)
    return svc.list_all()

@router.post("")
def create_{domain}(payload: dict, session: Session = Depends(get_session)):
    svc = {Pascal}Service(session)
    return svc.create(payload)
"""

(domain_dir / "models.py").write_text(models_py, encoding="utf-8")
(domain_dir / "repository.py").write_text(repository_py, encoding="utf-8")
(domain_dir / "service.py").write_text(service_py, encoding="utf-8")
(routers_dir / f"{domain}.py").write_text(router_py, encoding="utf-8")

# Cambio: registrar router en main.py con import absoluto desde app.routers
main_txt = main_file.read_text(encoding="utf-8")
import_line = f"from app.routers import {domain}"
if import_line not in main_txt:
    main_txt = import_line + "\n" + main_txt

include_line = f"app.include_router({domain}.router)"
if include_line not in main_txt:
    # Cambio: si ya hay include_router, añadimos una línea más; si no, lo pegamos al final
    if "app = FastAPI" in main_txt and "app.include_router" in main_txt:
        lines = main_txt.splitlines()
        # Inserta después del último include_router
        idx = max(i for i,l in enumerate(lines) if "app.include_router" in l)
        lines.insert(idx + 1, include_line)
        main_txt = "\n".join(lines) + "\n"
    else:
        main_txt += ("\n" + include_line + "\n")

main_file.write_text(main_txt, encoding="utf-8")

print(f"Dominio creado en: {domain_dir}")
print(f"Router creado en: {routers_dir / (domain + '.py')}")
print("Registrado en main.py")
