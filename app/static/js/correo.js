// VolleyDevByMaubry [23/∞] - Control de envío de correo con reCAPTCHA
document.addEventListener("DOMContentLoaded", () => {
  const formCorreo = document.getElementById("formCorreo");
  if (!formCorreo) return;

  formCorreo.addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = grecaptcha.getResponse();
    if (!token) {
      alert("Confirma el captcha antes de enviar.");
      return;
    }

    const datos = Object.fromEntries(new FormData(formCorreo));
    datos.token = token;

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

      if (!res.ok) throw new Error("No se pudo enviar");
      const json = await res.json();
      alert(json.mensaje);
      formCorreo.reset();
      grecaptcha.reset();
    } catch {
      alert("Error al enviar el correo");
      grecaptcha.reset();
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
