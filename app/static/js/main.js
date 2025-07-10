// VolleyDevByMaubry [8/∞]
let idActual = null;

document.addEventListener("DOMContentLoaded", async () => {
    await cargarPeliculas();
    await cargarGeneros();
    configurarEventos();
    configurarPreviewImagen();
});

function configurarEventos() {
    const btnCerrar = document.getElementById("cerrarSesion");
    if (btnCerrar) {
        btnCerrar.addEventListener("click", async () => {
            await fetch("/auth/logout");
            location.href = "/";
        });
    }

    const form = document.getElementById("formNuevaPelicula");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const datos = await obtenerDatosFormulario(form);
            const metodo = idActual ? "PUT" : "POST";
            const url = idActual ? `/pelicula/${idActual}` : "/pelicula/";

            try {
                const res = await fetch(url, {
                    method: metodo,
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datos)
                });

                if (!res.ok) throw new Error(await res.text());

                const json = await res.json();
                alert(json.mensaje);
                document.querySelector('[data-modal-hide="modalNuevaPelicula"]').click();
                await cargarPeliculas();
                form.reset();
                document.getElementById("previewFoto").classList.add("hidden");
                idActual = null;
            } catch (err) {
                alert("Error: " + err.message);
            }
        });
    }
}

async function obtenerDatosFormulario(form) {
    const formData = new FormData(form);
    const datos = Object.fromEntries(formData.entries());

    datos.codigo = parseInt(datos.codigo);
    datos.duracion = parseInt(datos.duracion);

    const archivo = form.foto?.files?.[0];
    if (archivo) {
        datos.foto = await toBase64(archivo);
    }

    return datos;
}

function configurarPreviewImagen() {
    const input = document.getElementById("inputFoto");
    const preview = document.getElementById("previewFoto");

    if (input && preview) {
        input.addEventListener("change", () => {
            const file = input.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = e => {
                preview.src = e.target.result;
                preview.classList.remove("hidden");
            };
            reader.readAsDataURL(file);
        });
    }
}

async function toBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = err => reject(err);
    });
}

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
            <td>
                ${p.foto ? `<img src="${p.foto}" class="w-16 h-16 object-cover rounded" />` : "N/A"}
            </td>
            <td>
                <button class="text-yellow-500" onclick="editarPelicula('${p.id}')">✏️</button>
                <button class="text-red-500 ml-2" onclick="eliminarPelicula('${p.id}')">🗑️</button>
            </td>
        `;
        tbody.appendChild(row);
    });

    if (!$.fn.DataTable.isDataTable('#tablaPeliculas')) {
        $('#tablaPeliculas').DataTable();
    }
}

async function cargarGeneros() {
    const res = await fetch("/genero/");
    const generos = await res.json();
    const select = document.getElementById("selectGeneros");
    select.innerHTML = `<option value="" disabled selected>Seleccione un género...</option>`;
    generos.forEach(g => {
        const option = document.createElement("option");
        option.value = g.id;
        option.textContent = g.nombre;
        select.appendChild(option);
    });
}

async function eliminarPelicula(id) {
    if (!confirm("¿Deseas eliminar esta película?")) return;
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

    if (p.foto) {
        const preview = document.getElementById("previewFoto");
        preview.src = p.foto;
        preview.classList.remove("hidden");
    }

    idActual = id;

    const modal = document.getElementById("modalNuevaPelicula");

    // 👇 Fallback si Flowbite no lo inicializó automáticamente
    if (!window.Flowbite?.instances?.getInstance(modal.id)) {
        const Modal = window.Modal || (await import('https://unpkg.com/flowbite@2.3.0')).Modal;
        new Modal(modal).show();
    } else {
        const instance = window.Flowbite.instances.getInstance(modal.id);
        instance.show();
    }
}
