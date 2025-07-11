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

    const formData = new FormData(formCorreo);
    formData.append("token", token);

    const boton = formCorreo.querySelector("button[type='submit']");
    boton.disabled = true;
    boton.textContent = "Enviando...";

    try {
      const res = await fetch("/correo/", {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error(await res.text());
      const json = await res.json();
      alert(json.mensaje);
      formCorreo.reset();
      grecaptcha.reset();
      cerrarModalCorreo();
    } catch (err) {
      alert("Error al enviar el correo: " + err.message);
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
