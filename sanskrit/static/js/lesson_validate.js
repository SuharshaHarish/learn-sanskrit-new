window.onload = function() {
  myFunction();
};

function myFunction() {
  var modal = document.getElementById("Modal");
  var modal_content = document.getElementById("Modal-content");
  var proceed_btn = document.getElementById("proceed_btn");

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks the button, open the modal

  modal.style.display = "none";
  modal_content.style.background = "#3498db";
  proceed_btn.style.background = "darkblue";
  document.getElementById("check_symbol").innerHTML =
    '<i class="fa fa-check"></i>';
  document.getElementById("crct").innerHTML = "Hurray!!! Its Correct!!!";
  // var w_modal = document.getElementById("wrong_Modal");
  // w_modal.style.display = "none";

  if (i < data.length) {
    var ques = data[i].fields.question;

    var ans = data[i].fields.answer;
    var q_type = data[i].fields.q_type;
    // var q_select = data[i].fields.q_select;
    // var q_jump = data[i].fields.q_jump;

    switch (q_type) {
      case "s":
        select_display();
        document.getElementsByClassName(
          "display"
        )[0].innerHTML = document.getElementById("select").innerHTML;
        document.getElementById("question").innerHTML = ques;
        //document.getElementById("choices").innerHTML = "ka";
        // document.getElementById("input").innerHTML = "<input type='text' id='ans1' /><br/>";
        //document.getElementById("select_submit").disabled = true;
        document.getElementById("submit").innerHTML =
          '<button id ="submit_btn" onclick= "validate()" type="button" disabled >Submit</button>';
        break;

      case "j":
        document.getElementsByClassName(
          "display"
        )[0].innerHTML = document.getElementById("jump").innerHTML;
        document.getElementById("question").innerHTML = ques;
        var words = ans.split(" ");
        var r = 0,
          r_used = [];
        for (j = 0; j < words.length; j++) {
          r = Math.floor(Math.random() * words.length);
          while (r_used.includes(r)) {
            r = Math.floor(Math.random() * words.length);
          }
          r_used.push(r);
          create_button(words[r]);
          // document.getElementById("ans_button").appendChild(btn);
        }
        //document.getElementById("final_ans").innerHTML = words[2];'<button id=j'+j+' onclick= "jump_ans('+this.id+');">'+words[j]+'</button>'
        console.log(words);
        document.getElementById("submit").innerHTML =
          '<button id ="submit_btn" onclick= "validate();">Submit</button>';
        break;

      case "t":
        document.getElementsByClassName(
          "display"
        )[0].innerHTML = document.getElementById("typing").innerHTML;
        document.getElementById("question").innerHTML = ques;
        //document.getElementsByClassName("input")[0].innerHTML = "<input type='text' id='input' /><br/>";
        document.getElementById("submit").innerHTML =
          '<button id ="submit_btn" onclick= "validate();">Submit</button>';

        Keyboard.init();
        break;

      default:
        console.log(q_type);
    }
  } else {
    document.getElementById("submit").innerHTML = "Bye";
  }
}

function validate() {
  var ans2 = data[i].fields.answer;
  var q_type = data[i].fields.q_type;

  switch (q_type) {
    case "s":
      var ans1 = selected_ans;
      break;

    case "j":
      var ans1 = strip(document.getElementById("final_ans").textContent);
      break;

    case "t":
      var ans1 = document.getElementById("typing_input").value;
      var kb = document.getElementsByClassName("keyboard");
      var kbh = document.getElementsByClassName("keyboard keyboard--hidden");
      for (var f = 0; f < kb.length || kbh.length; f++) {
        kb[f].className = "keyboard keyboard--hidden";
        kbh[f].parentNode.removeChild(kbh[f]);
      }
      break;
  }

  javascript: console.log(ans1);
  javascript: console.log(ans2);

  if (ans1 == ans2) {
    i++;
    document.getElementById("res").innerHTML = "Yes";
    // document.getElementById("check_ans").innerHTML = document.getElementById("right_Modal").innerHTML;
    // document.getElementById("right_css").innerHTML='<link rel="stylesheet" href="{% static "css/right.css" %}">';
    // document.getElementById("proceed_btn").innerHTML = '<button onclick= "myFunction();">Proceed</button>';

    var modal = document.getElementById("Modal");
    //var proceed_btn = document.getElementById("proceed_btn");
    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
    document.getElementById("check_symbol").innerHTML =
      '<i class="fa fa-check"></i>';
    // When the user clicks the button, open the modal

    modal.style.display = "block";
    // proceed_btn.style.background = "darkred";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
      i--;
      myFunction();
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if ((event.target = !modal)) {
        modal.style.display = "none";
      }
    };

    document.getElementById("crct").innerHTML = "HURRAY..!!! Its Correct!";
  } else {
    document.getElementById("res").innerHTML = "No";
    // document.getElementById("check_ans").innerHTML = document.getElementById("wrong_Modal").innerHTML;
    //  document.getElementById("wrong_css").innerHTML='<link rel="stylesheet" href="{% static "css/wrong.css" %}">';
    // document.getElementById("submit").innerHTML = '<button onclick= "myFunction();">Proceed</button>';

    var modal = document.getElementById("Modal");
    var modal_content = document.getElementById("Modal-content");
    var proceed_btn = document.getElementById("proceed_btn");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal

    modal.style.display = "block";
    modal_content.style.background = "#FF372D";
    proceed_btn.style.background = "darkred";
    document.getElementById("check_symbol").innerHTML =
      '<i class="fa fa-times"></i>';
    document.getElementById("crct").innerHTML = "Its Incorrect!!!";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
      myFunction();
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if ((event.target = !modal)) {
        modal.style.display = "none";
      }
    };
  }
}

function select_click(btn_id) {
  document.getElementById("submit_btn").disabled = false;
  //javascript: console.log(ans);
  selected_ans = document.getElementsByClassName("choices")[btn_id].textContent;
}

function select_display() {
  var ans2 = data[i].fields.answer;
  var x,
    y = 0,
    a = 0,
    b = 0,
    c = 0,
    d = 0,
    w = 0,
    z = 0;
  for (x = 0; x < ans_choice_data.length; x++) {
    var ans_choice = ans_choice_data[x].fields.ans_choice;
    if ((ans_choice = ans2)) {
      break;
    }
  }
  if (x == 0) {
    y = x + 1;
  }
  var a = Math.floor(Math.random() * 4);
  while (a == b) {
    b = Math.floor(Math.random() * 4);
  }
  while (c == a || c == b) {
    c = Math.floor(Math.random() * 4);
  }
  while (d == a || d == b || d == c) {
    d = Math.floor(Math.random() * 4);
  }

  while (w == x) {
    w = Math.floor(Math.random() * ans_choice_data.length);
  }
  while (y == x || y == w) {
    y = Math.floor(Math.random() * ans_choice_data.length);
  }
  while (z == w || z == x || z == y) {
    z = Math.floor(Math.random() * ans_choice_data.length);
  }
  // javascript: console.log(a);
  // javascript: console.log(b);
  // javascript: console.log(c);
  // javascript: console.log(d);

  // javascript: console.log(w);
  // javascript: console.log(x);
  // javascript: console.log(y);
  // javascript: console.log(z);
  document.getElementsByClassName("choices")[a].innerHTML =
    ans_choice_data[x].fields.ans_choice;
  document.getElementsByClassName("img-responsive")[a].src =
    "http://127.0.0.1:8000/media/" + ans_choice_data[x].fields.ans_image;
  document.getElementsByClassName("choices")[b].innerHTML =
    ans_choice_data[y].fields.ans_choice;
  document.getElementsByClassName("img-responsive")[b].src =
    "http://127.0.0.1:8000/media/" + ans_choice_data[y].fields.ans_image;
  document.getElementsByClassName("choices")[c].innerHTML =
    ans_choice_data[w].fields.ans_choice;
  document.getElementsByClassName("img-responsive")[c].src =
    "http://127.0.0.1:8000/media/" + ans_choice_data[w].fields.ans_image;
  document.getElementsByClassName("choices")[d].innerHTML =
    ans_choice_data[z].fields.ans_choice;
  document.getElementsByClassName("img-responsive")[d].src =
    "http://127.0.0.1:8000/media/" + ans_choice_data[z].fields.ans_image;
}

function jump_ans(j_id) {
  console.log(j_id);
  document.getElementById("final_ans").innerHTML =
    document.getElementById("final_ans").innerHTML +
    document.getElementById("" + j_id + "").textContent +
    " ";
  var used_btn = document.getElementById("" + j_id + "");
  used_btn.parentNode.removeChild(used_btn);
}

function create_button(word) {
  var btn = document.createElement("BUTTON");
  btn.innerHTML = word;
  btn.id = "j" + j;
  btn.onclick = function() {
    jump_ans(btn.id);
  };
  document.getElementById("ans_button").appendChild(btn);
  return;
}

function strip(str) {
  return str.replace(/^\s+|\s+$/g, "");
}
