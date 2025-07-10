// VolleyDevByMaubry [24/∞] — CRUD de Películas y Géneros

let idActual = null;
let generoActual = null;

document.addEventListener("DOMContentLoaded", async () => {
  const path = window.location.pathname;

  if (path.includes("/pelicula")) {
    await cargarPeliculas();
    await cargarGeneros();
    document.getElementById("formNuevaPelicula").addEventListener("submit", guardarPelicula);
    document.getElementById("fotoInput").addEventListener("input", previewFoto);
  }

  if (path.includes("/genero")) {
    await cargarGenerosTabla();
    document.getElementById("formGenero").addEventListener("submit", guardarGenero);
  }

  const cerrar = document.getElementById("cerrarSesion");
  if (cerrar) cerrar.addEventListener("click", async () => {
    await fetch("/auth/logout");
    location.href = "/";
  });
});

/* CRUD PELICULAS */
async function cargarPeliculas() {
  const res = await fetch("/pelicula/");
  const peliculas = await res.json();
  const tbody = document.querySelector("#tablaPeliculas tbody");
  tbody.innerHTML = "";
  peliculas.forEach(p => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${p.codigo}</td>
      <td>${p.titulo}</td>
      <td>${p.protagonista}</td>
      <td>${p.duracion}</td>
      <td>${p.resumen}</td>
      <td>${p.genero.nombre}</td>
      <td><img src="${p.foto || ''}" class="preview"></td>
      <td>
        <button onclick="editarPelicula('${p.id}')" class="btn-primary">✏️</button>
        <button onclick="eliminarPelicula('${p.id}')" class="btn-danger">🗑️</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

async function cargarGeneros() {
  const res = await fetch("/genero/");
  const generos = await res.json();
  const select = document.getElementById("selectGeneros");
  if (select) {
    select.innerHTML = `<option value="" disabled selected>Seleccione un género...</option>`;
    generos.forEach(g => {
      const option = document.createElement("option");
      option.value = g.id;
      option.textContent = g.nombre;
      select.appendChild(option);
    });
  }
}

async function guardarPelicula(e) {
  e.preventDefault();
  const form = e.target;
  const datos = Object.fromEntries(new FormData(form));
  datos.codigo = parseInt(datos.codigo);
  datos.duracion = parseInt(datos.duracion);

  const url = idActual ? `/pelicula/${idActual}` : "/pelicula/";
  const metodo = idActual ? "PUT" : "POST";

  try {
    const res = await fetch(url, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    });

    if (!res.ok) throw new Error(await res.text());
    const json = await res.json();
    alert(json.mensaje);
    cerrarModal();
    await cargarPeliculas();
    form.reset();
    idActual = null;
    document.getElementById("previewFoto").classList.add("hidden");
  } catch (err) {
    alert("Error: " + err.message);
  }
}

async function eliminarPelicula(id) {
  if (!confirm("¿Eliminar esta película?")) return;
  const res = await fetch(`/pelicula/${id}`, { method: "DELETE" });
  const json = await res.json();
  alert(json.mensaje);
  await cargarPeliculas();
}

async function editarPelicula(id) {
  const res = await fetch("/pelicula/");
  const peliculas = await res.json();
  const p = peliculas.find(p => p.id === id);
  if (!p) return alert("Película no encontrada");
  const form = document.getElementById("formNuevaPelicula");
  form.codigo.value = p.codigo;
  form.titulo.value = p.titulo;
  form.protagonista.value = p.protagonista;
  form.duracion.value = p.duracion;
  form.resumen.value = p.resumen;
  form.genero.value = p.genero.id;
  form.foto.value = p.foto || "";
  document.getElementById("previewFoto").src = p.foto || "";
  document.getElementById("previewFoto").classList.remove("hidden");
  idActual = id;
  abrirModal();
}

function previewFoto(e) {
  const url = e.target.value.trim();
  const img = document.getElementById("previewFoto");
  if (url) {
    img.src = url;
    img.classList.remove("hidden");
  } else {
    img.classList.add("hidden");
  }
}

function abrirModal() {
  document.getElementById("modalBackdrop").classList.add("show");
}
function cerrarModal() {
  document.getElementById("modalBackdrop").classList.remove("show");
}

/* CRUD GENEROS */
async function cargarGenerosTabla() {
  const res = await fetch("/genero/");
  const generos = await res.json();
  const tbody = document.querySelector("#tablaGeneros tbody");
  tbody.innerHTML = "";
  generos.forEach(g => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${g.nombre}</td>
      <td>
        <button onclick="editarGenero('${g.id}')" class="btn-primary">✏️</button>
        <button onclick="eliminarGenero('${g.id}')" class="btn-danger">🗑️</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

async function guardarGenero(e) {
  e.preventDefault();
  const form = e.target;
  const datos = Object.fromEntries(new FormData(form));
  const url = generoActual ? `/genero/${generoActual}` : "/genero/";
  const metodo = generoActual ? "PUT" : "POST";

  try {
    const res = await fetch(url, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    });

    if (!res.ok) throw new Error(await res.text());
    const json = await res.json();
    alert(json.mensaje);
    form.reset();
    cerrarModalGenero();
    await cargarGenerosTabla();
    generoActual = null;
  } catch (err) {
    alert("Error: " + err.message);
  }
}

async function eliminarGenero(id) {
  if (!confirm("¿Eliminar este género?")) return;
  const res = await fetch(`/genero/${id}`, { method: "DELETE" });
  const json = await res.json();
  alert(json.mensaje);
  await cargarGenerosTabla();
}

async function editarGenero(id) {
  const res = await fetch("/genero/");
  const generos = await res.json();
  const g = generos.find(g => g.id === id);
  if (!g) return alert("Género no encontrado");
  document.getElementById("formGenero").nombre.value = g.nombre;
  generoActual = id;
  abrirModalGenero();
}

function abrirModalGenero() {
  document.getElementById("modalGenero").classList.add("show");
}
function cerrarModalGenero() {
  document.getElementById("modalGenero").classList.remove("show");
}
