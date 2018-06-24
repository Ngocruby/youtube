// Set margins
var margin = {
  top: 100,
  right: 20,
  bottom: 30,
  left: 40
};
var width = 960 - margin.left - margin.right;
var height = 500 - margin.top - margin.bottom;

var tip2 = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function (d) {
    return "<strong>Total:</strong> <span style='color:red'>" + d.total + "</span>";
  });

// Add our chart to the #bar div
var svg = d3.select("#bar").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("id", "chart")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip2);

var genresForLand;
d3.json("./json/youtube.json", function (error, youtube) {
  genresForLand = youtube.genresForLand;

  //lay het tat ca cac key(ten cac nuoc), Object.keys de chuyen Object thanh array
  var countryKeys = Object.keys(genresForLand);

  // Dropdown Countries
  var myDiv = document.getElementById("myDiv");

  //Create and append select list
  var selectList = document.createElement("select");
  selectList.setAttribute("id", "mySelect");
  myDiv.appendChild(selectList);

  //Create and add the Options to the DropDownList.
  for (var i = 0; i < countryKeys.length; i++) {
    var option = document.createElement("option");
    option.setAttribute("value", countryKeys[i]);
    option.text = countryKeys[i];
    selectList.appendChild(option);
  }

  var country = countryKeys[0]; // take the 1st value on coutryKey (in this case: Afghanistan)

  var data = genresForLand[country];

  drawMap(data);
});

/* function type(d) {
  d.total = +d.total;
  return d;
} */

$(document).on('change', '#mySelect', function (event) { // phat hien thay do cua ID: mySelect
  var value = event.target.value; // Lay ten nuoc
  var data = genresForLand[value];// genre cho nuoc do
  drawMap(data);
});


function drawMap(data) {  // define ve bieu do vao 1 funktion
  $("#chart").html('');

  // x-Achse
  var x = d3.scaleBand()
    .rangeRound([0, width], .1)
    .padding(0.1);
  //y-Achse
  var y = d3.scaleLinear()
    .range([height, 0]);


  //Use our X scale to set a bottom axis
  var xAxis = d3.axisBottom(x)
  // Same for our left axis
  var yAxis = d3.axisLeft(y)

  data.forEach(function (d) {
    d.total = +d.total;
  });

  x.domain(data.map(function (d) {
    return d.genre;
  }));

  y.domain([0, d3.max(data, function (d) {
    return d.total;
  })]);

  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .attr("id", "bars")
    .attr("class", "x axis");

  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Total");

  svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function (d) {
      return x(d.genre);
    })
    .attr("width", x.bandwidth())
    .attr("y", function (d) {
      return y(d.total);
    })
    .attr("height", function (d) {
      return height - y(d.total);
    })
    .on('mouseover', tip2.show)
    .on('mouseout', tip2.hide);
}