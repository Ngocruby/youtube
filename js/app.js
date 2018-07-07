//Diese Datei ist aus D3-Bibliothek für das Zeichen des Music-Maps, inklusive Zoom-Funktion
var format = d3.format(",");

// Set tooltips
var tip = d3
  .tip()
  .attr("class", "d3-tip")
  .offset([-10, 0])
  .html(function (d) {
    return (
      "<strong>Country: </strong><span class='details'>" +
      d.properties.name +
      "<br></span>"
    );
  });

var width = window.outerWidth, // Feststellen Browser-Breite
  height = window.outerHeight; //Feststellen Browser-Höhe

var svg = d3
  .select("body") // Selectieren body-element
  .append("svg") // Hinzufügen svg zu body-element 
  .attr("id", "map") // Hinzufügen neue Attribute "id",
  .attr("width", width) // setzen die Breire für svg
  .attr("height", height) // setzen die Höhe für svg

var path = d3.geoPath();

var projection = d3
  .geoMercator() // projection Mercator erstellen
  .scale(150) // je mehr die Nummer ist, desto mehr zoomt es ein
  .translate([width / 2, height / 1.5]); // Koordinaten festlegen

var path = d3.geoPath().projection(projection);

svg.call(tip);

queue() 
  .defer(d3.json, "./json/world_countries.json") // Json Datei verlinken
  .defer(d3.json, "./json/youtube.json")
  .await(ready); //Funktion zu Weltkarte aufrufen

var player;

function ready(error, world_countries, youtube) {
  console.log(world_countries); 
  console.log(youtube);
  var videos = youtube.videos; // Objekt-videos und Objekt-overlay sind aus Datei youtube.json. Sie werden hier aufgerufen 
  var overlay = youtube.overlay;
  var top = youtube.top;

  player = new YT.Player("player", { //wireframe für Musik-Video
    height: "360",
    width: "400",
    videoId: top[0], // die ID von beliebtesten Video rausnehmen
    events: {
      onReady: onPlayerReady,
      onStateChange: onPlayerStateChange
    }
  });

  var g = svg.append("g")

  g.attr("class", "countries")
    .selectAll("path") //select all path in group countries
    .data(world_countries.features) //features is a object from world_countries
    .enter()
    .append("path") 
    .attr("d", path) 
    .attr("id", function (country) {
      var id = country.id; // Get Country ID in World Map
      var filterVideos = videos.filter(function (video) {
        return video.alpha3Code === id; // check if country ID in Videos is the same as country ID in World Map
      }); 
      if (filterVideos[0]) {
        // Check if video exists
        var videoId = filterVideos[0].video.id; // Get Video ID
        return videoId;
      }
      return "";
    })
    .style("fill", function (country) {
      var id = country.id; // Get Country ID in World Map
      var filterVideos = videos.filter(function (video) {
        return video.alpha3Code === id; // check if country ID in Videos is the same as country ID in World Map
      }); // return is truth or falsch like vs if
      if (filterVideos[0]) {
        // Check if video exists
        var videoId = filterVideos[0].video.id; // Get Video ID
        var color = overlay[videoId].color; // Get Color
        return color;
      }
      return "#aaaaaa";
    })
    .style("stroke", "white") // weiser Rand
    .style("stroke-width", 1.5) // Randbreite
    .style("opacity", 0.8) // transparent
    .on("click", function (d) {   // Video taucht auf wenn click auf jeden Land
      var id = d3.select(this).attr("id");

      player.loadVideoById({
        //load video
        videoId: id
      });
      player.playVideo(); // play video
    })
    .on("mouseover", function (d) {
      
      d3
        .select(this) // "this" wird automatisch als path wegen selectAll von oben versteht
        .style("opacity", 1)
        .style("stroke-width", 3);
      tip.show(d);
    })
    .on("mouseout", function (d) {
      
      d3
        .select(this)
        .style("opacity", 0.8)
        .style("stroke-width", 1.5);
      tip.hide(d);
    });

  // zoom and pan
  var zoom = d3.zoom().scaleExtent([1, 40]).on('zoom', () => {
    g.attr('transform', d3.event.transform) // updated for d3 v4
  });
  svg.call(zoom);
  // Resize
  d3.select(window).on('resize', () => {
    width = window.innerWidth;
    height = window.innerHeight;

    projection
      .scale(200)
      .translate([width / 2, height / 1.5]);

    d3.select("article").attr("width", width).attr("height", height);
    d3.select("svg#map").attr("width", width).attr("height", height);
    d3.selectAll("path").attr('d', path);
  });
  svg
    .append("path")
    .datum(topojson.mesh(world_countries.features, function (a, b) {
      return a.id !== b.id;
    }))
    // .datum(topojson.mesh(data.features, function(a, b) { return a !== b; }))
    .attr("class", "names")
    .attr("d", path);

  function onPlayerReady(event) { //start to load Video
    event.target.playVideo();
  }

  function onPlayerStateChange(event) { //repeat the Video
    if (event.data === YT.PlayerState.ENDED) {
      player.playVideo();
    }
  }
}

$('.player').click(function () {
  $('.player').toggleClass('active');
});