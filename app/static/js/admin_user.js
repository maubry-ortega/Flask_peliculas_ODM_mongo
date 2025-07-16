// VolleyDevByMaubry [11/∞] - La administración otorga el poder de crear.

/**
 * Archivo: static/js/admin_user.js
 * Autor: Maubry (VolleyDevByMaubry)
 *
 * Descripción:
 *     Script para gestionar usuarios desde el panel de administrador.
 *     Permite crear, editar y eliminar usuarios.
 *
 * Requisitos:
 *     - Nivel de acceso verificado desde backend.
 *     - El formulario debe tener id="formUsuario".
 *     - La tabla debe tener id="tablaUsuarios".
 */

let idUsuarioActual = null;

// Espera que el DOM esté cargado
document.addEventListener("DOMContentLoaded", async () => {
  await cargarUsuarios();
  
  document.getElementById("formUsuario").addEventListener("submit", guardarUsuario);
});

// Cargar lista de usuarios en la tabla
async function cargarUsuarios() {
  const res = await fetch("/admin/usuarios/api");
  const usuarios = await res.json();
  const tbody = document.querySelector("#tablaUsuarios tbody");
  tbody.innerHTML = "";

  usuarios.forEach(u => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${u.usuario}</td>
      <td>${u.nombre}</td>
      <td>${u.correo}</td>
      <td>${u.nivel}</td>
      <td>
        <button onclick="editarUsuario('${u.id}')" class="btn-primary">✏️</button>
        <button onclick="eliminarUsuario('${u.id}')" class="btn-danger">🗑️</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

// Guardar o actualizar usuario
async function guardarUsuario(e) {
  e.preventDefault();
  const form = e.target;
  const datos = Object.fromEntries(new FormData(form));

  const url = idUsuarioActual ? `/admin/usuarios/api/${idUsuarioActual}` : "/admin/usuarios/api";
  const metodo = idUsuarioActual ? "PUT" : "POST";

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
    cerrarModalUsuario();
    await cargarUsuarios();
    idUsuarioActual = null;
  } catch (err) {
    alert("Error: " + err.message);
  }
}

// Eliminar usuario
async function eliminarUsuario(id) {
  if (!confirm("¿Eliminar este usuario?")) return;
  const res = await fetch(`/admin/usuarios/api/${id}`, { method: "DELETE" });
  const json = await res.json();
  alert(json.mensaje);
  await cargarUsuarios();
}

// Editar usuario
async function editarUsuario(id) {
  const res = await fetch("/admin/usuarios/api");
  const usuarios = await res.json();
  const u = usuarios.find(u => u.id === id);
  if (!u) return alert("Usuario no encontrado");

  const form = document.getElementById("formUsuario");
  form.usuario.value = u.usuario;
  form.nombre.value = u.nombre;
  form.correo.value = u.correo;
  form.nivel.value = u.nivel;
  form.password.value = ""; // Solo cambiar si se edita manualmente

  idUsuarioActual = id;
  abrirModalUsuario();
}

// Mostrar modal
function abrirModalUsuario() {
  document.getElementById("modalUsuario").classList.add("show");
}

// Cerrar modal
function cerrarModalUsuario() {
  document.getElementById("modalUsuario").classList.remove("show");
}
