document.getElementById("cerrarSesion").addEventListener("click",async()=>{
  await fetch("/auth/logout");
  location.href="/";
});
