function ready(fn) {
  if (typeof fn !== "function") {
    throw new Error("Argument passed to ready should be a function");
  }

  if (document.readyState != "loading") {
    fn();
  } else if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", fn, {
      once: true,
    });
  } else {
    document.attachEvent("onreadystatechange", function () {
      if (document.readyState != "loading") fn();
    });
  }
}

function getData(url, page, successFunc) {
  if (page) {
    var page = parseInt(page);
  } else {
    var page = 1;
  }
  var empty_page = false;
  var block_request = false;
  var connect = true;
  window.onscroll = function () {
    var margin =
      document.documentElement.scrollHeight - window.innerHeight - 500;
    if (
      window.scrollY > margin &&
      empty_page == false &&
      block_request == false
    ) {
      block_request = true;
      if (connect) {
        page += 1;
      }
      var request = new XMLHttpRequest();
      request.onreadystatechange = function () {
        if (
          connect == false &&
          (this.readyState == 2 || this.readyState == 3)
        ) {
          connect = true;
          document.getElementById("connection-error").hidden = true;
        }
        if (this.readyState == 4 && this.status == 200) {
          var response = this.responseText;
          successFunc(response);
          block_request = false;
        } else if (this.readyState == 4 && this.status == 404) {
          empty_page = true;
          block_request = true;
        }
      };
      request.onerror = function () {
        document.getElementById("connection-error").hidden = false;
        connect = false;
        block_request = false;
      };
      request.open("GET", url + page, true);
      request.setRequestHeader("x-requested-with", "XMLHttpRequest");
      request.send();
    }
  };
}

function ajaxPost(url, loginUrl, button, successFunc) {
  var csrf = document.getElementById("csrf").querySelector("input").value;
  button.onclick = function (e) {
    var request = new XMLHttpRequest();
    var action = this.dataset.action;
    request.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        try {
          var response = JSON.parse(this.responseText);
        } catch (error) {
          window.location.replace(loginUrl);
        }
        successFunc(response, action);
      }
    };
    request.onerror = function () {
      document.getElementById("connection-error").hidden = false;
    };
    request.open("POST", url, true);
    request.setRequestHeader("X-CSRFToken", csrf);
    request.setRequestHeader("x-requested-with", "XMLHttpRequest");
    var data = new FormData();
    data.append("action", action);
    request.send(data);
  };
}
