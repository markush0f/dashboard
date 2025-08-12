# 🧠 Smart Monitor API

Aplicación backend desarrollada en **FastAPI** para el monitoreo inteligente de hábitos digitales. Utiliza **PostgreSQL** como base de datos y **Alembic** para la gestión de migraciones.

Este repositorio está diseñado con una arquitectura modular y desacoplada, pensada para escalar y mantener un código limpio.

---

## 🐳 Levantar Base de Datos y Herramientas

Archivo `docker-compose.yml` para ejecutar PostgreSQL, pgAdmin y Adminer

Para iniciar los servicios:

```bash
docker compose up -d
```

Acceso rápido:

* **FastAPI Docs** → [http://localhost:8000/docs](http://localhost:8000/docs)
* **pgAdmin** → [http://localhost:5050](http://localhost:5050) (usuario: admin\@local / contraseña: admin)
* **Adminer** → [http://localhost:8080](http://localhost:8080)

---

## ⚙️ Configuración de Alembic

1. **Instalar dependencias**

```bash
pip install alembic
```

2. **Inicializar Alembic**

```bash
python -m alembic init migrations
```

3. **Configurar conexión en `env.py`** para leer desde `settings.DATABASE_URL` y registrar metadatos de SQLModel.

---

## 📜 Comandos Útiles Alembic

* **Crear migración inicial**

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

* **Generar migración por cambios en modelos**

```bash
alembic revision --autogenerate -m "mensaje"
alembic upgrade head
```

* **Revertir último cambio**

```bash
alembic downgrade -1
```

---

## 🛠 Ejecución de Scripts de Migraciones

* **Linux/Mac**

```bash
./scripts/migrate.sh "mensaje de migración"
```

* **Windows**

```powershell
./scripts/migrate.ps1 "mensaje de migración"
```
