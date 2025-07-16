/**
 * VolleyDevByMaubry [11/∞] - Un acceso bien controlado es un sistema seguro.
 * 
 * login.js
 * Controla el flujo de login y la solicitud de nuevos usuarios.
 */

document.addEventListener("DOMContentLoaded", () => {
  const formLogin = document.getElementById("loginForm");
  const formSolicitud = document.getElementById("solicitudForm");

  formLogin?.addEventListener("submit", async e => {
    e.preventDefault();

    const token = grecaptcha.getResponse();
    if (!token) {
      alert("Completa el reCAPTCHA");
      return;
    }

    const usuario = formLogin.usuario.value;
    const password = formLogin.password.value;

    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario, password, token })
    });

    if (res.ok) {
      window.location = "/";
    } else {
      grecaptcha.reset();
      document.getElementById("error").classList.remove("hidden");
    }
  });

  document.getElementById("abrirSolicitudBtn").addEventListener("click", abrirModalSolicitud);

  formSolicitud?.addEventListener("submit", async e => {
    e.preventDefault();
    const datos = Object.fromEntries(new FormData(formSolicitud));
    
    const confirmacion = confirm("¿Deseas enviar esta solicitud al administrador?");
    if (!confirmacion) return;

    const res = await fetch("/correo/solicitud", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    });

    if (res.ok) {
      alert("Solicitud enviada correctamente.");
      cerrarModalSolicitud();
      formSolicitud.reset();
    } else {
      const json = await res.json();
      alert("Error: " + json.mensaje);
    }
  });
});

function abrirModalSolicitud() {
  document.getElementById("modalSolicitud").classList.remove("hidden");
}

function cerrarModalSolicitud() {
  document.getElementById("modalSolicitud").classList.add("hidden");
}
