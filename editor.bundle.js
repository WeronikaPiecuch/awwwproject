(function () {
  'use strict';

  // import CodeMirror from 'codemirror';
  // import 'codemirror/lib/codemirror.css';

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function clean_chosen() {
    var chosen = document.getElementsByClassName("chosen");
    for (var i = 0; i < chosen.length; i++) {
      chosen[i].classList.remove("chosen");
    }
    var chosen = document.getElementsByClassName("parent_chosen");
    for (var i = 0; i < chosen.length; i++) {
      chosen[i].classList.remove("parent_chosen");
    }
    if (document.getElementById("compile").classList.contains("show")) {
      document.getElementById("compile").classList.remove("show");
    }
    if (document.getElementById("download").classList.contains("show")) {
      document.getElementById("download").classList.remove("show");
    }
    if (document.getElementById("delete_file").classList.contains("show")) {
      document.getElementById("delete_file").classList.remove("show");
    }
    if (document.getElementById("delete_section").classList.contains("show")) {
      document.getElementById("delete_section").classList.remove("show");
    }
    if (document.getElementById("add_section").classList.contains("show")) {
      document.getElementById("add_section").classList.remove("show");
    }
    if (document.getElementById("delete_folder").classList.contains("show")) {
      document.getElementById("delete_folder").classList.remove("show");
    }

  }

  function clean_program() {
    document.getElementById("file_content").innerHTML = "  Wybierz plik z listy po lewej stronie";
    if (document.getElementById("add_section_info").classList.contains("show")) {
      document.getElementById("add_section_info").classList.remove("show");
    }
    if (document.getElementById("add_section_error").classList.contains("show")) {
      document.getElementById("add_section_error").classList.remove("show");
    }
  }

  function clean_fragment() {
    document.getElementById("fragment_content").innerHTML = "";
    if (document.getElementById("fragment_buttons").classList.contains("show")) {
      document.getElementById("fragment_buttons").classList.remove("show");
    }
  }

  function clean_highlight() {
    var highlight = document.getElementsByClassName("highlight");
    for (var i = 0; i < highlight.length; i++) {
      highlight[i].classList.remove("highlight");
    }
  }

  function sections_buttons() {
    var sections_headers = document.getElementsByClassName("section_header");
    for (var i = 0; i < sections_headers.length; i++) {
      sections_headers[i].addEventListener("click", (event) => {
        if (!event.target.parentElement.classList.contains("highlight")) {
          clean_highlight();
          event.target.parentElement.classList.add("highlight");
          if (!document.getElementById("delete_section").classList.contains("show")) {
            document.getElementById("delete_section").classList.add("show");
          }
        } else {
          event.target.parentElement.classList.remove("highlight");
          if (document.getElementById("delete_section").classList.contains("show")) {
            document.getElementById("delete_section").classList.remove("show");
          }
        }
      });
    }
    const lines = document.getElementsByClassName("line");
    for (var i = 0; i < lines.length; i++) {
      var range = document.createRange();
      range.selectNode(lines[i]);
    }
  }

  function add_section(event) {
    event.preventDefault();
    file_id = document.getElementsByClassName("chosen")[0].id.split("_")[1];
    const name = document.getElementById("section_name").value;
    const type = document.getElementById("section_type").value;
    fetch(`add/section/${file_id}/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        first_line: section_first_line,
        last_line: section_last_line,
        name: name,
        type: type,
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          document.getElementById("add_section_error").classList.add("show");
        } else {
          document.getElementById("file_content").innerHTML = data.content;
          sections_buttons();
          clean_fragment();
        }
        if (document.getElementById("delete_section").classList.contains("show")) {
          document.getElementById("delete_section").classList.remove("show");
        }
        showSectionUpload();
      });
  }

  const fileForm = document.getElementById("file_form");
  const folderForm = document.getElementById("folder_form");
  const section_form = document.getElementById("sectionUpload");
  fileForm.addEventListener("submit", add_file);
  folderForm.addEventListener("submit", add_folder);
  section_form.addEventListener("submit", add_section);
  var section_first_line = 0;
  var section_last_line = 0;

  function add_folder(event) {
    event.preventDefault();
    let parent_id = 0;
    if (document.getElementsByClassName("parent_chosen").length != 0) {
      parent_id = document.getElementsByClassName("parent_chosen")[0].id.split("_")[1];
    }
    const name = document.getElementById("folder_name").value;
    fetch(`add/folder/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        parent_id: parent_id,
        name: name,
      })
    })
      .then(response => response.json())
      .then(data => {
        clean_chosen();
        document.getElementById("navigation").innerHTML = data.structure;
        clean_program();
        clean_fragment();
        document.getElementById(`folder_${data.folder_id}`).classList.add("parent_chosen");
        document.getElementById("delete_folder").classList.add("show");
        showFolderUpload();
      });
  }

  function add_file(event) {
    event.preventDefault();
    let parent_id = 0;
    if (document.getElementsByClassName("parent_chosen").length != 0) {
      parent_id = document.getElementsByClassName("parent_chosen")[0].id.split("_")[1];
    }
    let name = document.getElementById("file_name").value;
    const file_src = document.getElementById("file_src").files[0];
    if (name == "") {
      name = file_src.name;
    }
    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        const file = reader.result;
        fetch(`add/file/`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify({
            parent_id: parent_id,
            name: name,
            file: file,
          })
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            clean_chosen();
            document.getElementById("navigation").innerHTML = data.structure;
            document.getElementById("file_content").innerHTML = data.file_content;
            if (document.getElementById("add_section_info").classList.contains("show")) {
              document.getElementById("add_section_info").classList.remove("show");
            }
            if (document.getElementById("add_section_error").classList.contains("show")) {
              document.getElementById("add_section_error").classList.remove("show");
            }
            sections_buttons();
            clean_fragment();
            document.getElementById(`file_${data.file_id}`).classList.add("chosen");
            document.getElementById("compile").classList.add("show");
            document.getElementById("delete_file").classList.add("show");
            document.getElementById("add_section").classList.add("show");
            const folder_li = document.getElementById(`file_${data.file_id}`).parentElement.parentElement.parentElement;
            if (folder_li.classList.contains("folder")) {
              const folder_button = folder_li.firstElementChild;
              folder_button.classList.add("parent_chosen");
              document.getElementById("delete_folder").classList.add("show");
            }
            showFileUpload();
          })
          .catch(error => {
            console.error('Error:', error);
          });
      },
      false
    );
    if (file_src) {
      reader.readAsText(file_src, "UTF-8");
    }
  }

  function clean_zalezne() {
    var chosen = document.getElementsByClassName("zalezne_form show");
    for (var i = 0; i < chosen.length; i++) {
      chosen[i].classList.remove("show");
    }
  }

  const standardForm = document.getElementById("standard_form");
  const optymalizacjeForm = document.getElementById("optymalizacje_form");
  const procesorForm = document.getElementById("procesor_form");
  const z80Form = document.getElementById("z80_form");
  const mcs51Form = document.getElementById("mcs51_form");
  const stm8Form = document.getElementById("stm8_form");
  standardForm.addEventListener("submit", standard);
  optymalizacjeForm.addEventListener("submit", optymalizacje);
  procesorForm.addEventListener("submit", procesor);
  z80Form.addEventListener("submit", (event) => zalezne(event, "z80"));
  mcs51Form.addEventListener("submit", (event) => zalezne(event, "mcs51"));
  stm8Form.addEventListener("submit", (event) => zalezne(event, "stm8"));

  function standard(event) {
    event.preventDefault();
    standard_id = document.querySelector('input[name="standard"]:checked').value;
    fetch(`standard/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        standard: standard_id,
      })
    })
      .then(response => response.json())
      .then(data => {
      });
  }

  function optymalizacje(event) {
    event.preventDefault();
    optymalizacje_list = document.querySelector('input[name="optymalizacje"]:checked');
    optymalizacje_id = [];
    for (var i = 0; i < optymalizacje_list.length; i++) {
      optymalizacje_id.push(optymalizacje_list[i].value);
    }
    fetch(`optymalizacje/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        optymalizacje: optymalizacje_id,
      })
    })
      .then(response => response.json())
      .then(data => {
      });
  }

  function procesor(event) {
    event.preventDefault();
    procesor_id = document.querySelector('input[name="procesor"]:checked').value;
    fetch(`procesor/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        procesor: procesor_id,
      })
    })
      .then(response => response.json())
      .then(data => {
      });
    clean_zalezne();
    procesor_id = procesor_id.toLowerCase();
    zalezneForm = document.getElementById(`${procesor_id}_form`);
    zalezneForm.classList.add("show");
  }

  function zalezne(event, procesor_id) {
    event.preventDefault();
    zalezne_id = document.querySelector(`input[name="${procesor_id}"]:checked`).value;
    fetch(`zalezne/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        procesor: procesor_id,
        opcje: zalezne_id,
      })
    })
      .then(response => response.json())
      .then(data => {
      });
  }
  function showFileUpload() {
    document.getElementById("fileUpload").classList.toggle("show");
    document.getElementById("blur").classList.toggle("show");
  }
  function showFolderUpload() {
    document.getElementById("folderUpload").classList.toggle("show");
    document.getElementById("blur").classList.toggle("show");
  }
  function showSectionUpload() {
    document.getElementById("sectionUpload").classList.toggle("show");
    document.getElementById("blur").classList.toggle("show");
  }
  window.onclick = function (e) {
    if (!e.target.matches('#plikDropbutton')) {
      document.getElementById("plikDropdown");
      if (plikDropdown.classList.contains('show')) {
        plikDropdown.classList.remove('show');
      }
    }
    if (!e.target.matches('#edycjaDropbutton')) {
      var edycjaDropdown = document.getElementById("edycjaDropdown");
      if (edycjaDropdown.classList.contains('show')) {
        edycjaDropdown.classList.remove('show');
      }
    }
    if (!e.target.matches('#opcjeDropbutton')) {
      var opcjeDropdown = document.getElementById("opcjeDropdown");
      if (opcjeDropdown.classList.contains('show')) {
        opcjeDropdown.classList.remove('show');
      }
    }
  };

})();
