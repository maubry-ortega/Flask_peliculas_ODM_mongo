let recaptchaCorreoId = null;

document.addEventListener("DOMContentLoaded", () => {
  const formCorreo = document.getElementById("formCorreo");
  if (!formCorreo) return;

  formCorreo.addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = grecaptcha.getResponse(recaptchaCorreoId);
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
      grecaptcha.reset(recaptchaCorreoId);
      cerrarModalCorreo();
    } catch (err) {
      alert("Error al enviar el correo: " + err.message);
      grecaptcha.reset(recaptchaCorreoId);
    } finally {
      boton.disabled = false;
      boton.textContent = "Enviar";
    }
  });
});

function abrirModalCorreo() {
  const modal = document.getElementById("modalCorreo");
  modal?.classList.add("show");

  if (typeof grecaptcha !== "undefined" && recaptchaCorreoId === null) {
    recaptchaCorreoId = grecaptcha.render("recaptchaContainerCorreo", {
      sitekey: siteKeyGlobal
    });
  }
}

function cerrarModalCorreo() {
  document.getElementById("modalCorreo")?.classList.remove("show");
}
