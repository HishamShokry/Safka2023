var cardValues = ["150", "200", "250", "600"]; // List of values for the card
var time = ["طلبات اليوم", "طلبات هذا الاسبوع", "طلبات هذا الشهر", "اجمالي الطلبات"];
var currentIndex = 0; // Index of the current value

function OrderschangeCard() {
  var cardNumber = document.getElementById('cardNumber');
  var cardText = document.getElementById('cardText');

  currentIndex = (currentIndex + 1) % cardValues.length; // Increment the index and wrap around

  cardNumber.innerHTML = cardValues[currentIndex];
  cardText.innerHTML = time[currentIndex];
  console.log(time[0]);
}