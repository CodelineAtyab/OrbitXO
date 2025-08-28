from __future__ import annotations
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import uuid
import threading

_LOCK = threading.Lock()

class RoutesRepository:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self._write([])

    def _read(self) -> List[Dict[str, Any]]:
        with _LOCK:
            if not self.config_path.exists():
                return []
            data = json.loads(self.config_path.read_text(encoding="utf-8") or "[]")
            if not isinstance(data, list):
                return []
            return data

    def _write(self, routes: List[Dict[str, Any]]) -> None:
        with _LOCK:
            self.config_path.write_text(json.dumps(routes, indent=2), encoding="utf-8")

    def list_routes(self) -> List[Dict[str, Any]]:
        return self._read()

    def add_route(self, route: Dict[str, Any]) -> Dict[str, Any]:
        routes = self._read()
        route = {**route}
        route.setdefault("id", str(uuid.uuid4()))
        routes.append(route)
        self._write(routes)
        return route

    def delete_route(self, route_id: str) -> bool:
        routes = self._read()
        new_routes = [r for r in routes if r.get("id") != route_id]
        changed = len(new_routes) != len(routes)
        if changed:
            self._write(new_routes)
        return changed

    def get(self, route_id: str) -> Optional[Dict[str, Any]]:
        for r in self._read():
            if r.get("id") == route_id:
                return r
        return None
