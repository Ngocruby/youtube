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

var width = window.outerWidth, // xac dinh chieu dai cua Browser -Detect Browser-Width
  height = window.outerHeight; //xac dinh chieu cao Detect Browser-Height

var svg = d3
  .select("body") // chon body element
  .append("svg") // them svg vao body - append la funktion
  .attr("id", "map")
  .attr("width", width) // set width for svg
  .attr("height", height) // set height for svg
/*
.append("g") // them element g vao trong svg - g viet tat cua group
.attr("class", "map"); // them attribu class ten map - add attribut
*/
var path = d3.geoPath();

var projection = d3
  .geoMercator() // tao projection Mercator
  .scale(150) // xet do zoom- so cang nho zoom cang nhieu
  .translate([width / 2, height / 1.5]); // xac dinh toa do

var path = d3.geoPath().projection(projection); // xac dinh duong ve theo projection

svg.call(tip);

queue() // bat dau xep hang
  .defer(d3.json, "./json/world_countries.json") // dan file json
  .defer(d3.json, "./json/youtube.json")
  .await(ready); // goi funktion ve ban do

var player;

function ready(error, world_countries, youtube) {
  console.log(world_countries); // log la in ra trong console
  console.log(youtube);
  var videos = youtube.videos; // videos va overlay la objekt trong file youtube goi ra de su dung
  var overlay = youtube.overlay;
  var top = youtube.top;

  player = new YT.Player("player", { //wireframe fuer Musik-Video
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
    .selectAll("path") // chon tat ca path trong group countries
    .data(world_countries.features) //features la objekt trong world_countries
    .enter()
    .append("path") // hanh dong ve
    .attr("d", path) // them atrribut net ve la d
    .attr("id", function (country) {
      var id = country.id; // Get Country ID in World Map
      var filterVideos = videos.filter(function (video) {
        return video.alpha3Code === id; // check if country ID in Videos is the same as country ID in World Mao
      }); // return la truth or falsch tuong duong vs if
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
        return video.alpha3Code === id; // check if country ID in Videos is the same as country ID in World Mao
      }); // return la truth or falsch tuong duong vs if
      if (filterVideos[0]) {
        // Check if video exists
        var videoId = filterVideos[0].video.id; // Get Video ID
        var color = overlay[videoId].color; // Get Color
        return color;
      }
      return "#aaaaaa";
    })
    .style("stroke", "white") // cho vien mau trang
    .style("stroke-width", 1.5) // do dam nhat cua vien
    .style("opacity", 0.8) // do transparent
    .on("click", function (d) {   // Video taucht auf wenn click auf jeden Land
      var id = d3.select(this).attr("id");

      player.loadVideoById({
        //load video
        videoId: id
      });
      player.playVideo(); // chay video
    })
    .on("mouseover", function (d) {
      // neu de chuot vao
      d3
        .select(this) // this dc tu hieu la path vi selectALL o tren
        .style("opacity", 1)
        .style("stroke-width", 3);
      tip.show(d);
    })
    .on("mouseout", function (d) {
      // neu di chuot ra
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