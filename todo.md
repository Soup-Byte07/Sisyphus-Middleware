# ✅ Proxy Framework TODO Checklist

## 📁 Core Framework Setup
- [ ] Finalize core directory structure (`core/`, `mod/`, `test/`, etc.)
- [ ] Create centralized `main.py` to initialize everything
- [ ] Automatically discover and load all mods from `/mod/`
- [ ] Initialize core services (cache, logging, shared utils)

---

## ⚙️ Routing & Proxy Logic

### 🧱 Route Factory
- [x] Implement `RouteFactory` with `create_router()` and `create_handler()`
- [x] Handle dynamic path parameters (`/item/{id}`)
- [x] Validate route definitions before registration
- [x] Support all HTTP methods: GET, POST, PUT, DELETE, PATCH
- [ ] Allow route-level pre/post hooks

### 🌐 Request Proxying
- [x] Forward headers, query params, path params, and body
- [ ] Handle JSON, form data, and multipart uploads
- [x] Return response status, headers, and content correctly
- [ ] Handle upstream timeouts and retries

---

## 🧩 Pxy Mods System

- [ ] Define and document the mod structure (`mod/my_mod/`)
- [ ] Support dynamic mod loading at runtime
- [x] Allow mods to register routes programmatically (not just via JSON)
- [ ] Enable lifecycle hooks (e.g. `on_load`, `on_request`)
- [ ] Validate mod schemas with helpful errors
- [ ] Provide helper types and abstract base classes for mods

---

## 🛠️ Core Services

### 🧠 Shared Utilities
- [X] Prevent circular dependencies by using a `shared/` module
- [ ] Centralize common types (`ProxyDefinition`, `RouteSpec`, etc.)

### 📦 Caching
- [ ] Add pluggable caching (in-memory by default)
- [ ] Support per-route or global cache configs
- [ ] Add cache expiry, invalidation options

### 📜 Logging
- [x] Implement centralized logging module
- [ ] Log requests/responses, errors, slow calls
- [ ] Optional: support structured logs or external log sinks (e.g. Sentry)

---

## 🧪 Testing & Debugging

- [ ] Set up test suite in `/test/` folder
- [ ] Test dynamic route creation and handler execution
- [ ] Validate correct proxying of all request types
- [ ] Simulate network errors, bad configs, and mod edge cases
- [ ] Add debug middleware (e.g. log full request/response objects)

---

## 🔐 Advanced Features (Optional)

- [ ] Add rate limiting/throttling support
- [ ] Support authentication/authorization for routes
- [ ] Implement retry logic and circuit breaker pattern
- [ ] Build a status endpoint or UI to inspect active mods/routes

---

## 📖 Documentation

- [ ] Write developer guide: “How to build a Pxy Mod”
- [ ] Include `mod/example_mod/` template
- [ ] Add a quickstart README with usage examples
- [ ] Document core types and APIs

---

