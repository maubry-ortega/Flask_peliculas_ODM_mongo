// VolleyDevByMaubry [25/∞] - Control de formulario de correo

document.addEventListener("DOMContentLoaded", () => {
  const formCorreo = document.getElementById("formCorreo");
  if (!formCorreo) return;

  formCorreo.addEventListener("submit", async (e) => {
    e.preventDefault();

    const datos = Object.fromEntries(new FormData(formCorreo));
    const boton = formCorreo.querySelector("button[type='submit']");
    boton.disabled = true;
    boton.textContent = "Enviando...";

    try {
      cerrarModalCorreo();

      const res = await fetch("/correo/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
      });

      if (!res.ok) throw new Error(await res.text());
      const json = await res.json();
      alert(json.mensaje);

      formCorreo.reset();
    } catch (err) {
      alert("Error al enviar el correo: " + err.message);
    } finally {
      boton.disabled = false;
      boton.textContent = "Enviar";
    }
  });
});

function abrirModalCorreo() {
  document.getElementById("modalCorreo")?.classList.add("show");
}

function cerrarModalCorreo() {
  document.getElementById("modalCorreo")?.classList.remove("show");
}
