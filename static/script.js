let expenseChart;
let transactions = JSON.parse(localStorage.getItem("transactions")) || [];

/* ========================= */
/* เพิ่มรายการ */
/* ========================= */

function addTransaction() {

    const date = document.getElementById("date").value;
    const detail = document.getElementById("detail").value;
    const amount = parseFloat(document.getElementById("amount").value);
    const type = document.getElementById("type").value;
    const category = document.getElementById("category").value;

    if (!date || !detail || !amount) {
        alert("กรอกข้อมูลให้ครบ");
        return;
    }

    const transaction = {
        id: Date.now(),
        date,
        detail,
        amount,
        type,
        category
    };

    transactions.push(transaction);

    localStorage.setItem(
        "transactions",
        JSON.stringify(transactions)
    );

    showTransactions();

    clearForm();
}

/* ========================= */
/* แสดงรายการ */
/* ========================= */

function showTransactions() {

    const transactionList =
        document.getElementById("transactionList");

    transactionList.innerHTML = "";

    let totalIncome = 0;
    let totalExpense = 0;

    let todayExpense = 0;
    let monthIncome = 0;
    let monthExpense = 0;

    const categorySummary = {};

    const now = new Date();

const today =
    now.getFullYear() + "-" +
    String(now.getMonth() + 1).padStart(2,"0") + "-" +
    String(now.getDate()).padStart(2,"0");

    const currentMonth =
        new Date().toISOString().slice(0,7);

    transactions.forEach(item => {

        /* ========================= */
        /* รวมรายรับรายจ่าย */
        /* ========================= */

        if (item.type === "income") {

            totalIncome += item.amount;

        } else {

            totalExpense += item.amount;
        }

        /* ========================= */
        /* วันนี้ใช้ไป */
        /* ========================= */

        if (
            item.type === "expense" &&
            item.date === today
        ) {

            todayExpense += item.amount;
        }

        /* ========================= */
        /* เดือนนี้ */
        /* ========================= */

        if(item.date.startsWith(currentMonth)){

            if(item.type === "income"){

                monthIncome += item.amount;
            }

            if(item.type === "expense"){

                monthExpense += item.amount;
            }
        }

        /* ========================= */
        /* หมวดใช้เยอะสุด */
        /* ========================= */

        if(item.type === "expense"){

            if(!categorySummary[item.category]){

                categorySummary[item.category] = 0;
            }

            categorySummary[item.category] += item.amount;
        }

        /* ========================= */
        /* ตาราง */
        /* ========================= */

        const row = `
            <tr>

                <td>${item.date}</td>

                <td>${item.detail}</td>

                <td>${item.category}</td>

                <td>
                    ${item.type === "income"
                        ? "รายรับ"
                        : "รายจ่าย"}
                </td>

                <td>
                    ${item.amount.toLocaleString()} บาท
                </td>

                <td>

                    <button
                        class="delete-btn"
                        onclick="deleteTransaction(${item.id})">

                        ลบ

                    </button>

                </td>

            </tr>
        `;

        transactionList.innerHTML += row;
    });

    /* ========================= */
    /* ใช้เยอะสุด */
    /* ========================= */

    let topCategory = "-";
    let max = 0;

    for (const category in categorySummary){

        if(categorySummary[category] > max){

            max = categorySummary[category];

            topCategory = category;
        }
    }

    /* ========================= */
    /* SUMMARY */
    /* ========================= */

    document.getElementById("totalIncome").innerText =
        totalIncome.toLocaleString() + " บาท";

    document.getElementById("totalExpense").innerText =
        totalExpense.toLocaleString() + " บาท";

    document.getElementById("balance").innerText =
        (totalIncome - totalExpense).toLocaleString() + " บาท";

    /* ========================= */
    /* DASHBOARD */
    /* ========================= */

    document.getElementById("todayExpense").innerText =
        todayExpense.toLocaleString() + " บาท";

    document.getElementById("monthIncome").innerText =
        monthIncome.toLocaleString() + " บาท";

    document.getElementById("monthExpense").innerText =
        monthExpense.toLocaleString() + " บาท";

    document.getElementById("topCategory").innerText =
        topCategory;

    /* ========================= */
    /* CHART */
    /* ========================= */

    updateChart();
}

/* ========================= */
/* ลบรายการ */
/* ========================= */

function deleteTransaction(id) {

    transactions = transactions.filter(
        item => item.id !== id
    );

    localStorage.setItem(
        "transactions",
        JSON.stringify(transactions)
    );

    showTransactions();
}

/* ========================= */
/* ล้างฟอร์ม */
/* ========================= */

function clearForm() {

    document.getElementById("date").value = "";
    document.getElementById("detail").value = "";
    document.getElementById("amount").value = "";
}

/* ========================= */
/* Dark Mode */
/* ========================= */

function toggleDarkMode() {

    document.body.classList.toggle("dark-mode");
}

/* ========================= */
/* โหลดครั้งแรก */
/* ========================= */

showTransactions();
/* ========================= */
/* CHART */
/* ========================= */



/* ========================= */
/* อัปเดตกราฟ */
/* ========================= */

function updateChart() {

    const expenseData = {};

    transactions.forEach(item => {

        if (item.type === "expense") {

            if (!expenseData[item.category]) {
                expenseData[item.category] = 0;
            }

            expenseData[item.category] += item.amount;
        }
    });

    const labels = Object.keys(expenseData);

    const data = Object.values(expenseData);

    const ctx =
        document.getElementById("expenseChart");

    /* ========================= */
    /* กันกราฟซ้อน */
    /* ========================= */

    if (expenseChart) {
        expenseChart.destroy();
    }

    expenseChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: labels,

            datasets: [{

                label: "รายจ่าย",

                data: data,

                backgroundColor: [
                    "#ff6384",
                    "#36a2eb",
                    "#ffce56",
                    "#4bc0c0",
                    "#9966ff"
                ],

                borderWidth: 2
            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {
                    position: "bottom"
                }
            }
        }
    });
}