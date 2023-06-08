CodeMirror.defineMode("text/x-csrc-with-asm", function () {
  var cKeywords = {
    // ...
  };

  var asmSectionRules = [
    {
      regex: /__asm\b[\s\S]*?\b__endasm\b/g,
      token: "asm-section"
    }
  ];

  return {
    startState: function () {
      return { inAsmSection: false };
    },
    token: function (stream, state) {
      if (stream.match(/^__asm\b/)) {
        state.inAsmSection = true;
        return "asm-section";
      }

      if (state.inAsmSection) {
        if (stream.match(/^.*?__endasm\b/)) {
          state.inAsmSection = false;
        }
        stream.skipToEnd();
        return "asm-section";
      }

      // Inne reguły dla składni C
      // ...

      stream.next();
      return null;
    },
    // Inne metody i właściwości dla analizatora składni C z obsługą sekcji asemblerowych
    // ...
  };
});

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
  if (document.getElementById("save").classList.contains("show")) {
    document.getElementById("save").classList.remove("show");
  }
  if (document.getElementById("download").classList.contains("show")) {
    document.getElementById("download").classList.remove("show");
  }
  if (document.getElementById("delete_file").classList.contains("show")) {
    document.getElementById("delete_file").classList.remove("show");
  }
  // if (document.getElementById("delete_section").classList.contains("show")) {
  //   document.getElementById("delete_section").classList.remove("show");
  // }
  // if (document.getElementById("add_section").classList.contains("show")) {
  //   document.getElementById("add_section").classList.remove("show");
  // }
  if (document.getElementById("delete_folder").classList.contains("show")) {
    document.getElementById("delete_folder").classList.remove("show");
  }

}

function clean_program() {
  document.getElementById("file_content").innerHTML = "  Wybierz plik z listy po lewej stronie";
  // if (document.getElementById("add_section_info").classList.contains("show")) {
  //   document.getElementById("add_section_info").classList.remove("show")
  // }
  // if (document.getElementById("add_section_error").classList.contains("show")) {
  //   document.getElementById("add_section_error").classList.remove("show")
  // }
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
    })
  }
  const lines = document.getElementsByClassName("line");
  for (var i = 0; i < lines.length; i++) {
    var range = document.createRange();
    range.selectNode(lines[i]);
  }
}

function show_add_section() {
  var selection = window.getSelection();
  if (selection.toString() == "") {
    if (!document.getElementById("add_section_info").classList.contains("show")) {
      document.getElementById("add_section_info").classList.add("show")
    }
  } else {
    if (document.getElementById("add_section_info").classList.contains("show")) {
      document.getElementById("add_section_info").classList.remove("show")
    }
    if (document.getElementById("add_section_error").classList.contains("show")) {
      document.getElementById("add_section_error").classList.remove("show")
    }
    const lines = document.getElementsByClassName("line");
    var first_line = lines.length + 1;
    var last_line = 0;
    for (var i = 0; i < lines.length; i++) {
      if (selection.containsNode(lines[i])) {
        const num = lines[i].id.split("_")[1];
        first_line = Math.min(first_line, num);
        last_line = Math.max(last_line, num);
      }
    }
    const first_id = selection.anchorNode.parentNode.id;
    const last_id = selection.focusNode.parentNode.id;
    if (first_id.split("_")[0] == "line") {
      first_line = Math.min(first_line, first_id.split("_")[1]);
      last_line = Math.max(last_line, first_id.split("_")[1]);
    }
    if (last_id.split("_")[0] == "line") {
      last_line = Math.max(last_line, last_id.split("_")[1]);
      first_line = Math.min(first_line, last_id.split("_")[1]);
    }
    section_first_line = first_line;
    section_last_line = last_line;
    var legend = document.getElementById("section_legend");
    legend.innerHTML = "Wybrano linie od " + first_line + " do " + last_line;
    showSectionUpload();
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
    })
}

function file(file_id) {
  if (document.getElementById("file_" + file_id).classList.contains("chosen")) {
    clean_chosen();
    clean_program();
    clean_fragment();
  } else {
    fetch(`/file/${file_id}`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      }
    })
      .then(response => response.json())
      .then(data => {
        // document.getElementById("file_content").innerHTML = data.content;
        // if (document.getElementById("add_section_info").classList.contains("show")) {
        //   document.getElementById("add_section_info").classList.remove("show")
        // }
        // if (document.getElementById("add_section_error").classList.contains("show")) {
        //   document.getElementById("add_section_error").classList.remove("show")
        // }
        // sections_buttons();
        // clean_fragment();
        // let editor = new EditorView({
        //   doc: data.content,
        //   extensions: [basicSetup, javascript()],
        //   parent: document.body
        // })
        document.getElementById("file_content").innerHTML = "";
        CodeMirror(document.querySelector('#file_content'), {
          lineNumbers: true,
          tabSize: 4,
          value: data.content,
          mode: "text/x-csrc-with-asm",
          theme: "default",
        });
        // editor.addOverlay({
        //   token: function (stream) {
        //     // Kolorowanie sekcji asemblerowych
        //     if (stream.match(/__asm[\s\S]*?__endasm/, false)) {
        //       return "asm-section";
        //     }
        //     // Zwróć null, aby wskazać brak kolorowania
        //     stream.next();
        //     return null;
        //   }
        // });
      })
    clean_chosen();
    const file_button = document.getElementById(`file_${file_id}`);
    file_button.classList.add("chosen");
    document.getElementById("compile").classList.add("show");
    document.getElementById("save").classList.add("show");
    // document.getElementById("delete_file").classList.add("show");
    // document.getElementById("add_section").classList.add("show");
    const folder_li = file_button.parentElement.parentElement.parentElement;
    if (folder_li.classList.contains("folder")) {
      const folder_button = folder_li.firstElementChild;
      folder_button.classList.add("parent_chosen");
      document.getElementById("delete_folder").classList.add("show");
    }
  }
}

function save_file() {
  file_id = document.getElementsByClassName("chosen")[0].id.split("_")[1];
  const content = document.getElementsByClassName("CodeMirror")[0].CodeMirror.getValue();
  fetch(`save/${file_id}/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({
      content: content,
    })
  })
    .then(response => response.json())
    .then(data => {
    })

}

function folder(folder_id) {
  if (document.getElementById(`folder_${folder_id}`).classList.contains("parent_chosen") && document.getElementsByClassName("chosen").length == 0) {
    clean_chosen();
    clean_program();
    clean_fragment();
  } else {
    clean_chosen();
    document.getElementById(`folder_${folder_id}`).classList.add("parent_chosen");
    clean_program();
    clean_fragment();
    document.getElementById("delete_folder").classList.add("show");
  }
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
    })
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
          document.getElementById("file_content").innerHTML = "";
          var editor = CodeMirror(document.querySelector('#file_content'), {
            lineNumbers: true,
            tabSize: 4,
            value: data.content,
            mode: "text/x-csrc-with-asm",
            theme: "default",
            // lineAttributes: function (line) {
            //   // Tworzenie odpowiednich atrybutów dla każdej linii
            //   var lineNumber = line.lineNo();
            //   var lineId = "line_" + lineNumber;
            //   return {
            //     "id": lineId
            //   };
            // }
          });
          // if (document.getElementById("add_section_info").classList.contains("show")) {
          //   document.getElementById("add_section_info").classList.remove("show")
          // }
          // if (document.getElementById("add_section_error").classList.contains("show")) {
          //   document.getElementById("add_section_error").classList.remove("show")
          // }
          // sections_buttons();
          clean_fragment();
          document.getElementById(`file_${data.file_id}`).classList.add("chosen");
          document.getElementById("compile").classList.add("show");
          document.getElementById("save").classList.add("show");
          // document.getElementById("delete_file").classList.add("show");
          // document.getElementById("add_section").classList.add("show");
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

function delete_file() {
  file_id = document.getElementsByClassName("chosen")[0].id.split("_")[1];
  clean_chosen();
  fetch(`delete/file/${file_id}`, {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("navigation").innerHTML = data.structure;
      clean_fragment();
    })
}

function delete_folder() {
  folder_id = document.getElementsByClassName("parent_chosen")[0].id.split("_")[1];
  clean_chosen();
  fetch(`delete/folder/${folder_id}`, {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("navigation").innerHTML = data.structure;
      clean_program();
    })
}

function compile() {
  file_id = document.getElementsByClassName("chosen")[0].id.split("_")[1];
  fetch(`compile/${file_id}`, {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("fragment_content").innerHTML = data.compile;
      // document.getElementById("file_content").innerHTML = data.content;
      // if (document.getElementById("add_section_info").classList.contains("show")) {
      //   document.getElementById("add_section_info").classList.remove("show")
      // }
      // if (document.getElementById("add_section_error").classList.contains("show")) {
      //   document.getElementById("add_section_error").classList.remove("show")
      // }
      // sections_buttons();
      document.getElementById("download").classList.add("show");
      if (data.compiled) {
        document.getElementById("fragment_buttons").classList.add("show");
      }
      const asm_sections = document.getElementsByClassName("asm_section_header");
      for (var i = 0; i < asm_sections.length; i++) {
        asm_sections[i].addEventListener("click", (event) => {
          id = event.target.id.split("_")[2];
          document.getElementById("asm_content_" + id).classList.toggle("show");
        })
      }
      // const errors = document.getElementsByClassName("error_section");
      // for (var i = 0; i < errors.length; i++) {
      //   errors[i].addEventListener("mousedown", (event) => {
      //     id = event.target.id.split("_")[1];
      //     document.getElementsByClassName("line_" + id)[0].classList.add("highlight");
      //     document.getElementsByClassName("line_" + id)[0].scrollIntoView();
      //     event.target.classList.add("highlight");
      //   })
      //   errors[i].addEventListener("mouseup", (event) => {
      //     id = event.target.id.split("_")[1];
      //     document.getElementsByClassName("line_" + id)[0].classList.remove("highlight");
      //     event.target.classList.remove("highlight");
      //   })
      // }
      // const asm_lines = document.getElementsByClassName("asm_line");
      // for (var i = 0; i < asm_lines.length; i++) {
      //   asm_lines[i].addEventListener("mousedown", (event) => {
      //     id = event.target.id.split("_")[2];
      //     document.getElementsByClassName("line_" + id)[0].classList.add("highlight");
      //     document.getElementsByClassName("line_" + id)[0].scrollIntoView();
      //     event.target.classList.add("highlight");
      //   })
      //   asm_lines[i].addEventListener("mouseup", (event) => {
      //     id = event.target.id.split("_")[2];
      //     document.getElementsByClassName("line_" + id)[0].classList.remove("highlight");
      //     event.target.classList.remove("highlight");
      //   })
      // }
    })
}

function download() {
  file_id = document.getElementsByClassName("chosen")[0].id.split("_")[1];
  fetch(`download/${file_id}`, {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }
  })
}

function delete_section() {
  file_id = document.getElementsByClassName("chosen")[0].id.split("_")[1];
  section_id = document.getElementsByClassName("highlight")[0].id.split("_")[1];
  fetch(`delete/section/${file_id}/${section_id}`, {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("file_content").innerHTML = data.content;
      if (document.getElementById("add_section_info").classList.contains("show")) {
        document.getElementById("add_section_info").classList.remove("show")
      }
      if (document.getElementById("add_section_error").classList.contains("show")) {
        document.getElementById("add_section_error").classList.remove("show")
      }
      sections_buttons();
      clean_fragment();
      document.getElementById("delete_section").classList.remove("show");
    })
}

function clean_zalezne() {
  var chosen = document.getElementsByClassName("zalezne_form show");
  for (var i = 0; i < chosen.length; i++) {
    chosen[i].classList.remove("show");
  }
}

function show_asm() {
  asm_sections = document.getElementsByClassName("asm_section_content");
  for (var i = 0; i < asm_sections.length; i++) {
    if (!asm_sections[i].classList.contains("show")) {
      asm_sections[i].classList.add("show");
    }
  }
}

function hide_asm() {
  asm_sections = document.getElementsByClassName("asm_section_content");
  for (var i = 0; i < asm_sections.length; i++) {
    if (asm_sections[i].classList.contains("show")) {
      asm_sections[i].classList.remove("show");
    }
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
    })
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
    })
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
    })
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
    })
}


function plikFunction() {
  document.getElementById("plikDropdown").classList.toggle("show");
}
function edycjaFunction() {
  document.getElementById("edycjaDropdown").classList.toggle("show");
}
function opcjeFunction() {
  document.getElementById("opcjeDropdown").classList.toggle("show");
}
function standardFunction() {
  document.getElementById("standard_tab").style.display = "block";
  document.getElementById("optymalizacje_tab").style.display = "none";
  document.getElementById("procesor_tab").style.display = "none";
  document.getElementById("zalezne_tab").style.display = "none";
  if (!document.getElementById("standard").classList.contains("chosen")) {
    document.getElementById("standard").classList.add("chosen")
  }
  if (document.getElementById("optymalizacje").classList.contains("chosen")) {
    document.getElementById("optymalizacje").classList.remove("chosen")
  }
  if (document.getElementById("procesor").classList.contains("chosen")) {
    document.getElementById("procesor").classList.remove("chosen")
  }
  if (document.getElementById("zalezne").classList.contains("chosen")) {
    document.getElementById("zalezne").classList.remove("chosen")
  }
}
function optymalizacjeFunction() {
  document.getElementById("standard_tab").style.display = "none";
  document.getElementById("optymalizacje_tab").style.display = "block";
  document.getElementById("procesor_tab").style.display = "none";
  document.getElementById("zalezne_tab").style.display = "none";
  if (document.getElementById("standard").classList.contains("chosen")) {
    document.getElementById("standard").classList.remove("chosen")
  }
  if (!document.getElementById("optymalizacje").classList.contains("chosen")) {
    document.getElementById("optymalizacje").classList.add("chosen")
  }
  if (document.getElementById("procesor").classList.contains("chosen")) {
    document.getElementById("procesor").classList.remove("chosen")
  }
  if (document.getElementById("zalezne").classList.contains("chosen")) {
    document.getElementById("zalezne").classList.remove("chosen")
  }
}
function procesorFunction() {
  document.getElementById("standard_tab").style.display = "none";
  document.getElementById("optymalizacje_tab").style.display = "none";
  document.getElementById("procesor_tab").style.display = "block";
  document.getElementById("zalezne_tab").style.display = "none";
  if (document.getElementById("standard").classList.contains("chosen")) {
    document.getElementById("standard").classList.remove("chosen")
  }
  if (document.getElementById("optymalizacje").classList.contains("chosen")) {
    document.getElementById("optymalizacje").classList.remove("chosen")
  }
  if (!document.getElementById("procesor").classList.contains("chosen")) {
    document.getElementById("procesor").classList.add("chosen")
  }
  if (document.getElementById("zalezne").classList.contains("chosen")) {
    document.getElementById("zalezne").classList.remove("chosen")
  }
}
function zalezneFunction() {
  document.getElementById("standard_tab").style.display = "none";
  document.getElementById("optymalizacje_tab").style.display = "none";
  document.getElementById("procesor_tab").style.display = "none";
  document.getElementById("zalezne_tab").style.display = "block";
  if (document.getElementById("standard").classList.contains("chosen")) {
    document.getElementById("standard").classList.remove("chosen")
  }
  if (document.getElementById("optymalizacje").classList.contains("chosen")) {
    document.getElementById("optymalizacje").classList.remove("chosen")
  }
  if (document.getElementById("procesor").classList.contains("chosen")) {
    document.getElementById("procesor").classList.remove("chosen")
  }
  if (!document.getElementById("zalezne").classList.contains("chosen")) {
    document.getElementById("zalezne").classList.add("chosen")
  }
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
    var plikropdown = document.getElementById("plikDropdown");
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
}
