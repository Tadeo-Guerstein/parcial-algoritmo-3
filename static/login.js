const URL = "http://127.0.0.1:8000";
const username = document.getElementById("username");
const form = document.querySelector("form");

async function handleSubmit(event) {
  event.preventDefault();

  const user = username.value;

  const response = await fetch(`${URL}/login`, {
    method: "POST",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: user }), // Cambiado de 'username' a 'name'
  });

  window.location.href = "http://127.0.0.1:8000/customers";
}

form.onsubmit = handleSubmit;
