const URL = "http://localhost:8000";
const tableContainer = document.querySelector(".table-responsive");
const emptyText = document.getElementById("empty-text");
const form = document.querySelector("form");
const inputGroup = document.getElementById("grupo");
const tbody = document.querySelector("tbody");
const logout = document.getElementById("logout");

async function getOrders() {
    const customerID = sessionStorage.getItem("customerID");
    const response = await fetch(`${URL}/order/${customerID}`);
    if (response.status === 200) return await response.json();
}

function isLogged() {
    let flag = true;
    if (!sessionStorage.getItem("customerID")) {
        window.location.href = "/";
        flag = false;
    }
    return flag;
}

async function handleOnLoad() {
    if (!isLogged()) return;
    const { data: orders } = await getOrders();
    if (orders.length > 0) {
        clearTable();
        fillOrderTable(orders);
        return;
    }
    const span = document.createElement("span");
    span.id = "empty-text";
    span.innerText = "No hay datos para listar";
    tableContainer.appendChild(span);
}

function clearTable() {
    const rows = tbody.rows.length;
    for (let i = 0; i < rows; i++) {
        tbody.deleteRow(0);
    }
}
function fillOrderTable(data) {
    data.forEach((i) => {
        const tBodyRow = tbody.insertRow();
        const tBodyCellId = tBodyRow.insertCell();
        const tBodyCellName = tBodyRow.insertCell();
        const tBodyCellActionName = tBodyRow.insertCell();

        tBodyCellId.innerText = i.id;
        tBodyCellName.innerText = i.orderName;
        tBodyCellActionName.innerText = i.customerID?.join(", ") || "Sin usuarios asignados";
    });
}

async function handleOnSubmit(event) {
    event.preventDefault();
    const name = inputGroup.value;
    const customerID = sessionStorage.getItem("customerID");
    await fetch(`${URL}/order`, {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ customerID: customerID, orderName: name }),
    });
    await handleOnLoad();
}

async function handleLogout() {
    const customerID = sessionStorage.getItem("customerID");
    const response = await fetch(`${URL}/logout/${customerID}`, {
        method: "PUT",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    sessionStorage.removeItem("customerID");
    window.location.href = "/";
}

document.onload = handleOnLoad();
form.onsubmit = handleOnSubmit;
logout.addEventListener("click", handleLogout);

let isNavigating = undefined;
window.addEventListener("beforeunload", () => {isNavigating ?? handleLogout();});
window.addEventListener("click", (event) => { if (event.target.tagName === "A" && event.target.href) isNavigating = true; });
window.addEventListener("load", () => { isNavigating = undefined; });
