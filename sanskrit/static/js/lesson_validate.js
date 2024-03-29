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
  document.getElementById("crct").innerHTML = "Well Done!!! Its Correct!!!";
  if (i < data.length) {
    
    var q_type = data[i].fields.q_type;

    var question_translate = document.createElement("div");
    question_translate.id = "question_translate";


    var description = data[i].fields.description;
    if (description && description.length>0) {      
      display_decription(description, q_type);        
    }
    else{
      display_question();
    }

  } else {
    // End of lesson
    document.getElementById("submit").innerHTML =
      '<button id ="continue_btn" type="button" >Continue learning</button>';
    $("#continue_btn").click(function() {
      
      $.ajax({
        url: lesson_complete_url,
        data: {
          completed: "True",
          lesson_name: lesson_name
        },
        dataType: "json",
        success: function(data) {
          if (data.completed == "True") {
            window.location.href =
              lessons_url
          }
        }
      });
    });
  }
}

function display_question(){

  var ques = data[i].fields.question;
  var ans = data[i].fields.answer;
  var q_type = data[i].fields.q_type;

  var question_translate = document.createElement("div");
  question_translate.id = "question_translate";

  switch (q_type) {
    case "s":
      select_display();
      document.getElementsByClassName(
        "display"
      )[0].innerHTML = document.getElementById("select").innerHTML;
      document.getElementById("question").innerHTML = `<span>${ques}</span>`;
      document.getElementById("submit").innerHTML =
        '<button id ="submit_btn" onclick= "validate()" type="button" disabled >Submit</button>';

      question_translate.innerHTML =
        '<button id="question_translate_btn" onclick="question_translate();"><i class="fas fa-volume-up"></i></button>';
      document.getElementById("question").appendChild(question_translate);
      break;

    case "j":
      document.getElementsByClassName(
        "display"
      )[0].innerHTML = document.getElementById("jump").innerHTML;
      document.getElementById("question").innerHTML = `<span>${ques}</span>`;
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
      }
      document.getElementById("submit").innerHTML =
        '<button id ="submit_btn" onclick= "validate();">Submit</button>';

      question_translate.innerHTML =
        '<button id="question_translate_btn" onclick="question_translate();"><i class="fas fa-volume-up"></i></button>';
      document.getElementById("question").appendChild(question_translate);
      break;

    case "t":
      document.getElementsByClassName(
        "display"
      )[0].innerHTML = document.getElementById("typing").innerHTML;
      document.getElementById("question").innerHTML = `<span>${ques}</span>`;
      document.getElementById("submit").innerHTML =
        '<button id ="submit_btn" onclick= "validate();">Submit</button>';

      Keyboard.init();

      question_translate.innerHTML =
        '<button id="question_translate_btn" onclick="question_translate();"><i class="fas fa-volume-up"></i></button>';
      document.getElementById("question").appendChild(question_translate);
      break;

    default:
      console.log(q_type);
  }

}

function display_decription(description, q_type) {
  
  var desc_img = data[i].fields.desc_image;
  var desc_img_src = media_url + desc_img;

  document.getElementsByClassName(
    "display"
  )[0].innerHTML = document.getElementById("description").innerHTML;
  document.getElementById("desc_text").innerHTML = description;
  document.getElementById("submit").innerHTML =
    '<button id ="continue_btn" type="button" onclick= "display_question();" >Proceed</button>';

  // Resize Image
  var canvas = document.getElementById("canvas");
  var img = new Image();

  img.onload = function() {
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    var MAX_WIDTH = 400;
    var MAX_HEIGHT = 400;
    var width = img.width;
    var height = img.height;

    if (width > height) {
      if (width > MAX_WIDTH) {
        height *= MAX_WIDTH / width;
        width = MAX_WIDTH;
      }
    } else {
      if (height > MAX_HEIGHT) {
        width *= MAX_HEIGHT / height;
        height = MAX_HEIGHT;
      }
    }
    canvas.width = width;
    canvas.height = height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, width, height);
  };
  img.src = desc_img_src;
  // document.getElementById("desc_img") = img;
  return;
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

  if (ans1 == ans2) {
    i++;
    // correct answer audio
    let src = correct_audio_src;
    let audio = new Audio(src);
    audio.play();

    var modal = document.getElementById("Modal");
    var span = document.getElementsByClassName("close")[0];
    document.getElementById("check_symbol").innerHTML =
      '<i class="fa fa-check"></i>';
    modal.style.display = "block";

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
    // wrong answer audio
    let src = wrong_audio_src;
    let audio = new Audio(src);
    audio.play();

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
  // Progress Bar width
  var progress_bar = document.getElementsByClassName("progress-bar")[0];
  progress_percent = (i / data.length) * 100;
  progress_bar.style.width = progress_percent + "%";
}

function select_click(btn_id) {
  document.getElementById("submit_btn").disabled = false;
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
  document.getElementsByClassName("choices")[a].innerHTML =
    ans_choice_data[x].fields.ans_choice;
  document.getElementsByClassName("icon1")[a].src =
    media_url + ans_choice_data[x].fields.ans_image;
  document.getElementsByClassName("choices")[b].innerHTML =
    ans_choice_data[y].fields.ans_choice;
  document.getElementsByClassName("icon1")[b].src =
    media_url + ans_choice_data[y].fields.ans_image;
  document.getElementsByClassName("choices")[c].innerHTML =
    ans_choice_data[w].fields.ans_choice;
  document.getElementsByClassName("icon1")[c].src =
    media_url + ans_choice_data[w].fields.ans_image;
  document.getElementsByClassName("choices")[d].innerHTML =
    ans_choice_data[z].fields.ans_choice;
  document.getElementsByClassName("icon1")[d].src =
    media_url + ans_choice_data[z].fields.ans_image;
}

function jump_ans(j_id) {
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

// GTTS
function question_translate() {
  
  $.ajax({
    url: translate_audio_url,
    data: {
      text: data[i].fields.question
    },
    dataType: "json",
    success: function(data) {
      if (data) {
        let src = media_url + data.audio_src;        
        let audio = new Audio(src);
        audio.play();
      }
    }
  });
  
}
