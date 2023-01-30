"use strict";
const d = document;
d.addEventListener("DOMContentLoaded", function (event) {
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: "btn btn-primary me-3",
      cancelButton: "btn btn-gray",
    },
    buttonsStyling: false,
  });

  // options
  const breakpoints = {
    sm: 540,
    md: 720,
    lg: 960,
    xl: 1140,
  };

  var sidebar = document.getElementById("sidebarMenu");
  if (sidebar && d.body.clientWidth < breakpoints.lg) {
    sidebar.addEventListener("shown.bs.collapse", function () {
      document.querySelector("body").style.position = "fixed";
    });
    sidebar.addEventListener("hidden.bs.collapse", function () {
      document.querySelector("body").style.position = "relative";
    });
  }

  var iconNotifications = d.querySelector(".notification-bell");
  if (iconNotifications) {
    iconNotifications.addEventListener("shown.bs.dropdown", function () {
      iconNotifications.classList.remove("unread");
    });
  }

  [].slice.call(d.querySelectorAll("[data-background]")).map(function (el) {
    el.style.background = "url(" + el.getAttribute("data-background") + ")";
  });

  [].slice.call(d.querySelectorAll("[data-background-lg]")).map(function (el) {
    if (document.body.clientWidth > breakpoints.lg) {
      el.style.background =
        "url(" + el.getAttribute("data-background-lg") + ")";
    }
  });

  [].slice
    .call(d.querySelectorAll("[data-background-color]"))
    .map(function (el) {
      el.style.background =
        "url(" + el.getAttribute("data-background-color") + ")";
    });

  [].slice.call(d.querySelectorAll("[data-color]")).map(function (el) {
    el.style.color = "url(" + el.getAttribute("data-color") + ")";
  });

  //Tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Popovers
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Datepicker
  var datepickers = [].slice.call(d.querySelectorAll("[data-datepicker]"));
  var datepickersList = datepickers.map(function (el) {
    return new Datepicker(el, {
      buttonClass: "btn",
    });
  });

  if (d.querySelector(".input-slider-container")) {
    [].slice
      .call(d.querySelectorAll(".input-slider-container"))
      .map(function (el) {
        var slider = el.querySelector(":scope .input-slider");
        var sliderId = slider.getAttribute("id");
        var minValue = slider.getAttribute("data-range-value-min");
        var maxValue = slider.getAttribute("data-range-value-max");

        var sliderValue = el.querySelector(":scope .range-slider-value");
        var sliderValueId = sliderValue.getAttribute("id");
        var startValue = sliderValue.getAttribute("data-range-value-low");

        var c = d.getElementById(sliderId),
          id = d.getElementById(sliderValueId);

        noUiSlider.create(c, {
          start: [parseInt(startValue)],
          connect: [true, false],
          //step: 1000,
          range: {
            min: [parseInt(minValue)],
            max: [parseInt(maxValue)],
          },
        });
      });
  }

  if (d.getElementById("input-slider-range")) {
    var c = d.getElementById("input-slider-range"),
      low = d.getElementById("input-slider-range-value-low"),
      e = d.getElementById("input-slider-range-value-high"),
      f = [d, e];

    noUiSlider.create(c, {
      start: [
        parseInt(low.getAttribute("data-range-value-low")),
        parseInt(e.getAttribute("data-range-value-high")),
      ],
      connect: !0,
      tooltips: true,
      range: {
        min: parseInt(c.getAttribute("data-range-value-min")),
        max: parseInt(c.getAttribute("data-range-value-max")),
      },
    }),
      c.noUiSlider.on("update", function (a, b) {
        f[b].textContent = a[b];
      });
  }

  //Chartist

  var data = JSON.parse(document.getElementById("actions_json").textContent);
  if (d.querySelector(".ct-chart-sales-value")) {
    new Chartist.Line(
      ".ct-chart-sales-value",
      {
        labels: Object.keys(data),
        series: [Object.values(data)],
      },
      {
        low: 0,
        showArea: true,
        fullWidth: true,
        plugins: [Chartist.plugins.tooltip()],
        axisX: {
          showGrid: false,
        },
        axisY: {
          showGrid: false,
          showLabel: false,
        },
      }
    );
  }

  function setChartData(chartName) {
    var data = JSON.parse(
      document.getElementById(chartName + "_json").textContent
    );
    if (d.querySelector("." + chartName + "-chart")) {
      var chart = new Chartist.Bar(
        "." + chartName + "-chart",
        {
          labels: Object.keys(data),
          series: [Object.values(data)],
        },
        {
          reverseData: true,
          plugins: [Chartist.plugins.tooltip()],
          axisY: {
            showGrid: false,
            showLabel: false,
            offset: 0,
          },
        }
      );

      chart.on("draw", function (data) {
        if (data.type === "line" || data.type === "area") {
          data.element.animate({
            d: {
              begin: 2000 * data.index,
              dur: 2000,
              from: data.path
                .clone()
                .scale(1, 0)
                .translate(0, data.chartRect.height())
                .stringify(),
              to: data.path.clone().stringify(),
              easing: Chartist.Svg.Easing.easeOutQuint,
            },
          });
        }
      });
    }
  }

  setChartData("users");
  setChartData("posts");
  setChartData("contacts");

  if (d.getElementById("loadOnClick")) {
    d.getElementById("loadOnClick").addEventListener("click", function () {
      var button = this;
      var loadContent = d.getElementById("extraContent");
      var allLoaded = d.getElementById("allLoadedText");

      button.classList.add("btn-loading");
      button.setAttribute("disabled", "true");

      setTimeout(function () {
        loadContent.style.display = "block";
        button.style.display = "none";
        allLoaded.style.display = "block";
      }, 1500);
    });
  }

  var scroll = new SmoothScroll('a[href*="#"]', {
    speed: 500,
    speedAsDuration: true,
  });

  if (d.querySelector(".current-year")) {
    d.querySelector(".current-year").textContent = new Date().getFullYear();
  }

  // Glide JS

  if (d.querySelector(".glide")) {
    new Glide(".glide", {
      type: "carousel",
      startAt: 0,
      perView: 3,
    }).mount();
  }

  if (d.querySelector(".glide-testimonials")) {
    new Glide(".glide-testimonials", {
      type: "carousel",
      startAt: 0,
      perView: 1,
      autoplay: 2000,
    }).mount();
  }

  if (d.querySelector(".glide-clients")) {
    new Glide(".glide-clients", {
      type: "carousel",
      startAt: 0,
      perView: 5,
      autoplay: 2000,
    }).mount();
  }

  if (d.querySelector(".glide-news-widget")) {
    new Glide(".glide-news-widget", {
      type: "carousel",
      startAt: 0,
      perView: 1,
      autoplay: 2000,
    }).mount();
  }

  if (d.querySelector(".glide-autoplay")) {
    new Glide(".glide-autoplay", {
      type: "carousel",
      startAt: 0,
      perView: 3,
      autoplay: 2000,
    }).mount();
  }

  // Pricing countup
  var billingSwitchEl = d.getElementById("billingSwitch");
  if (billingSwitchEl) {
    const countUpStandard = new countUp.CountUp("priceStandard", 99, {
      startVal: 199,
    });
    const countUpPremium = new countUp.CountUp("pricePremium", 199, {
      startVal: 299,
    });

    billingSwitchEl.addEventListener("change", function () {
      if (billingSwitch.checked) {
        countUpStandard.start();
        countUpPremium.start();
      } else {
        countUpStandard.reset();
        countUpPremium.reset();
      }
    });
  }
});
