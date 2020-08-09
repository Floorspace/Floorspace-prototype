
function leaveChange() {

document.getElementById('root').innerHTML = "";

// const logo = document.createElement('img')
// logo.src = 'logo.png'

const container = document.createElement('div')
container.setAttribute('class', 'container')

// app.appendChild(logo)
app.appendChild(container)

var e = document.getElementById("cities");
var cityName = e.options[e.selectedIndex].value;

console.log(cityName);

var ctype = document.getElementById("constructionTypes");
var constructionType = ctype.options[ctype.selectedIndex].value;

console.log(constructionType);

var ltype = document.getElementById("languages");
var language = ltype.options[ltype.selectedIndex].value;

console.log(language);

// Create a request variable and assign a new XMLHttpRequest object to it.
var request = new XMLHttpRequest()

// Open a new connection, using the GET request on the URL endpoint
request.open('GET', 'http://localhost:8080/FS-backend/v1.0/ad-info/all-ads-with-filters?city='+cityName+"&constructionType="+constructionType + "&filterLanguages="+language, true)

request.setRequestHeader('Content-type', 'application/json');
request.setRequestHeader('Access-Control-Allow-Origin', '*')
request.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, PUT')
request.setRequestHeader('Access-Control-Allow-Headers',' Origin, Content-Type, Accept, Authorization, X-Request-With')
request.setRequestHeader('Access-Control-Allow-Credentials',' true');
// request.setRequestHeader('Access-Control-Request-Headers','Content-Type, Authorization');

request.onload = function () {
  // console.log(request.status);
  // console.log(request.statusText);
  if (request.readyState == 4 && request.status == 200) {
    // myFunction(xmlhttp.responseText);

    var data = JSON.parse(this.response)

	for (var i = 0; i < data.length; i++) {
	    var counter = data[i];
	    // console.log(counter.commonDetails.propertyType);
	    // console.log(counter.commonDetails.constructionType);
	    // console.log(counter.commonDetails.city);
	    // console.log(counter.commonDetails.address);
	    // console.log(counter.commonDetails.description);
	    // console.log(counter.commonDetails.propertyCost);
	    // console.log(counter.commonDetails.numOfPoolMembers);

	    // console.log(counter.houseconstructionAdDetails.existingFloors);
	    // console.log(counter.houseconstructionAdDetails.floorSpaceArea);
	    // console.log(counter.houseconstructionAdDetails.floorSpaceArea);
	    // console.log(counter.houseconstructionAdDetails.lengthOfFloorSpace);
	    // console.log(counter.houseconstructionAdDetails.breadthOfFloorSpace);
	    // console.log(counter.houseconstructionAdDetails.numOfAllowedFloorsForConstruction);

	      var cons_type = counter.commonDetails.constructionType;

		  const card = document.createElement('div')
	      card.setAttribute('class', 'card')
		  card.style.cssText = "width:500px;height:200px;border:2px solid #000"


	      const h1 = document.createElement('h2')
	      h1.textContent = counter.commonDetails.propertyType + " floor space in " + counter.commonDetails.city

	      const address = document.createElement('h3')
	      address.textContent = "Property address: "+counter.commonDetails.address

		  const area = document.createElement('h3')
	      if(cons_type == "FLOOR_HOUSE_CONSTRUCTION"){

	      		area.textContent = "Property area: "+counter.houseconstructionAdDetails.floorSpaceArea
	      }
	      else if(cons_type == "APARTMENT_CONSTRUCTION"){

	      		area.textContent = "Property area: "+counter.apartmentConstructionAdDetails.apartmentArea
	      }


	      const cost = document.createElement('h3')
	      cost.textContent = "Property cost: "+counter.commonDetails.propertyCost


	      container.appendChild(card)
	      card.appendChild(h1)
	      card.appendChild(address)
	      card.appendChild(area)
	      card.appendChild(cost)


	}
  }
  else{
  	console.log("Error")
  }
};

request.send()

}




const app = document.getElementById('root')

// const logo = document.createElement('img')
// logo.src = 'logo.png'

const container = document.createElement('div')
container.setAttribute('class', 'container')

// app.appendChild(logo)
app.appendChild(container)

var e = document.getElementById("cities");
var cityName = e.options[e.selectedIndex].value;

console.log(cityName);

var ctype = document.getElementById("constructionTypes");
var constructionType = ctype.options[ctype.selectedIndex].value;

console.log(constructionType);

var ltype = document.getElementById("languages");
var language = ltype.options[ltype.selectedIndex].value;

console.log(language);

// Create a request variable and assign a new XMLHttpRequest object to it.
var request = new XMLHttpRequest()

// Open a new connection, using the GET request on the URL endpoint
request.open('GET', 'http://localhost:8080/FS-backend/v1.0/ad-info/all-ads-with-filters?city='+cityName+"&constructionType="+constructionType + "&filterLanguages="+language, true)

request.setRequestHeader('Content-type', 'application/json');
request.setRequestHeader('Access-Control-Allow-Origin', '*')
request.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, PUT')
request.setRequestHeader('Access-Control-Allow-Headers',' Origin, Content-Type, Accept, Authorization, X-Request-With')
request.setRequestHeader('Access-Control-Allow-Credentials',' true');
// request.setRequestHeader('Access-Control-Request-Headers','Content-Type, Authorization');

request.onload = function () {
  // console.log(request.status);
  // console.log(request.statusText);
  if (request.readyState == 4 && request.status == 200) {
    // myFunction(xmlhttp.responseText);

    var data = JSON.parse(this.response)

	for (var i = 0; i < data.length; i++) {
	    var counter = data[i];
	    // console.log(counter.commonDetails.propertyType);
	    // console.log(counter.commonDetails.constructionType);
	    // console.log(counter.commonDetails.city);
	    // console.log(counter.commonDetails.address);
	    // console.log(counter.commonDetails.description);
	    // console.log(counter.commonDetails.propertyCost);
	    // console.log(counter.commonDetails.numOfPoolMembers);

	    // console.log(counter.houseconstructionAdDetails.existingFloors);
	    // console.log(counter.houseconstructionAdDetails.floorSpaceArea);
	    // console.log(counter.houseconstructionAdDetails.floorSpaceArea);
	    // console.log(counter.houseconstructionAdDetails.lengthOfFloorSpace);
	    // console.log(counter.houseconstructionAdDetails.breadthOfFloorSpace);
	    // console.log(counter.houseconstructionAdDetails.numOfAllowedFloorsForConstruction);

		  const card = document.createElement('div')
	      card.setAttribute('class', 'card')
		  card.style.cssText = "width:500px;height:200px;border:2px solid #000"


	      const h1 = document.createElement('h2')
	      h1.textContent = counter.commonDetails.propertyType + " floor space in " + counter.commonDetails.city

	      const address = document.createElement('h3')
	      address.textContent = "Property address: "+counter.commonDetails.address

	      const area = document.createElement('h3')
	      area.textContent = "Property area: "+counter.houseconstructionAdDetails.floorSpaceArea

	      const cost = document.createElement('h3')
	      cost.textContent = "Property cost: "+counter.commonDetails.propertyCost


	      container.appendChild(card)
	      card.appendChild(h1)
	      card.appendChild(address)
	      card.appendChild(area)
	      card.appendChild(cost)


	}
  }
  else{
  	console.log("Error")
  }
};

request.send()






// const app = document.getElementById('root')

// const logo = document.createElement('img')
// logo.src = 'logo.png'

// const container = document.createElement('div')
// container.setAttribute('class', 'container')

// app.appendChild(logo)
// app.appendChild(container)

// var request = new XMLHttpRequest()
// request.open('GET', 'https://ghibliapi.herokuapp.com/films', true)
// request.onload = function () {
//   // Begin accessing JSON data here
//   var data = JSON.parse(this.response)
//   if (request.status >= 200 && request.status < 400) {
//     data.forEach((movie) => {
//       const card = document.createElement('div')
//       card.setAttribute('class', 'card')

//       const h1 = document.createElement('h1')
//       h1.textContent = movie.title

//       const p = document.createElement('p')
//       movie.description = movie.description.substring(0, 300)
//       p.textContent = `${movie.description}...`

//       container.appendChild(card)
//       card.appendChild(h1)
//       card.appendChild(p)
//     })
//   } else {
//     const errorMessage = document.createElement('marquee')
//     errorMessage.textContent = `Gah, it's not working!`
//     app.appendChild(errorMessage)
//   }
// }

// request.send()
