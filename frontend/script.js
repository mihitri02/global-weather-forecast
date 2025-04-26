const body = document.getElementById('body');
const cityInput = document.getElementById('cityInput');
const suggestions = document.getElementById('suggestions');
const weatherCard = document.getElementById('weatherCard');
const locationEl = document.getElementById('location');
const iconEl = document.getElementById('icon');
const descriptionEl = document.getElementById('description');
const tempEl = document.getElementById('temp');
const humidityEl = document.getElementById('humidity');

// Example Static City List (you can expand later)
const cities = ["Mumbai", "Delhi", "Bangalore", "New York", "London", "Tokyo", "Paris", "Sydney", "Toronto", "Dubai", "Ahmedabad", "Pune", "Vadodara", "Rajkot", "Surat", "Gandhinagar", "Jaipur", "Kolkata"];

cityInput.addEventListener('input', () => {
  const input = cityInput.value.toLowerCase();
  suggestions.innerHTML = '';
  if (input.length === 0) return;

  const filtered = cities.filter(city => city.toLowerCase().includes(input));
  filtered.forEach(city => {
    const li = document.createElement('li');
    li.classList.add('list-group-item');
    li.textContent = city;
    li.onclick = () => {
      cityInput.value = city;
      suggestions.innerHTML = '';
      getWeather(city);
    };
    suggestions.appendChild(li);
  });
});

async function getWeather(city) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/weather?city=${city}`);
    const data = await response.json();
    if (response.ok) {
      locationEl.textContent = data.city;
      iconEl.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
      descriptionEl.textContent = data.description;
      tempEl.textContent = data.temperature;
      humidityEl.textContent = data.humidity;
      weatherCard.style.display = 'block';
    } else {
      alert(data.error || "Weather data not found!");
    }
  } catch (error) {
    alert("Error fetching weather data.");
  }
}

// Background based on Time
function setTheme() {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 12) {
    body.classList.add('morning');
  } else if (hour >= 12 && hour < 18) {
    body.classList.add('afternoon');
  } else {
    body.classList.add('night');
  }
}
setTheme();
