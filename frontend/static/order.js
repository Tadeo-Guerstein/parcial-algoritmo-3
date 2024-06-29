const URL = 'http://localhost:8000'
const tableContainer = document.querySelector('.table-responsive')
const emptyText = document.getElementById('empty-text')
const form = document.querySelector('form')
const inputGroup = document.getElementById('grupo')
const tbody = document.querySelector('tbody')
const logout = document.getElementById('logout')

async function getGrupos() {
  const customerID = localStorage.getItem('customerID')
  const response = await fetch(`${URL}/order/${customerID}`)
  if (response.status === 200) {
    return await response.json()
  }
}

async function handleOnLoad() {
  const { data: grupos } = await getGrupos()
  if (grupos.length > 0) {
    const rows = tbody.rows.length
    for (let i = 0; i < rows; i++) {
      tbody.deleteRow(0)
    }
    grupos.forEach((i) => {
      const tBodyRow = tbody.insertRow()
      const tBodyCellId = tBodyRow.insertCell()
      const tBodyCellName = tBodyRow.insertCell()
      const tBodyCellFechaPedido = tBodyRow.insertCell()
      const tBodyCellActionName = tBodyRow.insertCell()

      tBodyCellId.innerText = i.id;
      tBodyCellName.innerText = i.orderName;
      tBodyCellFechaPedido.innerText = i.orderDate;
      tBodyCellActionName.innerText = i.customer || 'Sin usuarios asignados'
    })
    return
  }
  const span = document.createElement('span')
  span.id = 'empty-text'
  span.innerText = 'No hay datos para listar'
  tableContainer.appendChild(span)
}

async function handleOnSubmit(event) {
  event.preventDefault()
  const name = inputGroup.value
  const customerID = localStorage.getItem('customerID')
  await fetch(`${URL}/order`, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customerID:customerID, orderName:name }),
  });
  await handleOnLoad();
}

async function handleOnClickLogout() {
    const customerID = localStorage.getItem("customerID");
    const response = await fetch(`${URL}/logout/${customerID}`, {
        method: "PUT",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();

    if (response.status !== 200) {
        alert(data.error);
        return;
    }

    window.location.href = "/";
}

document.onload = handleOnLoad()
form.onsubmit = handleOnSubmit
logout.onclick = handleOnClickLogout
