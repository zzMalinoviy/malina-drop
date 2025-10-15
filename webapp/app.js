window.Telegram.WebApp.expand();

function openCase() {
  fetch("/open_case", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ initData: Telegram.WebApp.initData })
  })
  .then(res => res.json())
  .then(data => {
    const gif = document.createElement("img");
    gif.src = data.gif_url;
    gif.className = "drop-animation";
    document.body.appendChild(gif);

    setTimeout(() => {
      alert(`🎉 Вы получили: ${data.item_name} (${data.rarity})`);
      document.getElementById("inventory-list").innerHTML += `<li>${data.item_name}</li>`;
    }, 3000);
  });
}

function buyItem() {
  alert("✅ Покупка успешна!");
  document.getElementById("inventory-list").innerHTML += "<li>🎧 Неоновые наушники</li>";
}

function applyPromo() {
  const code = document.getElementById("promoInput").value;
  fetch("/promo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ initData: Telegram.WebApp.initData, code: code })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message);
  });
}
