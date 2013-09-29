var categories = [[89, 'Aerospace Engineering'],
 [88, 'Agricultural Engineering'],
 [102, 'Algebra'],
 [10, 'Anatomy'],
 [131, 'Anesthesiology'],
 [25, 'Anthropology'],
 [77, 'Applied Computer Science'],
 [107, 'Applied Physics'],
 [127, 'Archaeology'],
 [94, 'Art'],
 [58, 'Astrophysics'],
 [78, 'Atmospheric Sciences'],
 [108, 'Atomic Physics'],
 [11, 'Behavioral neuroscience'],
 [4, 'Biochemistry'],
 [125, 'Bioinformatics'],
 [42, 'Biological engineering'],
 [1, 'Biophysics'],
 [21, 'Biotechnology'],
 [65, 'Botany'],
 [64, 'Cancer'],
 [140, 'Cardiology'],
 [12, 'Cell biology'],
 [137, 'Cheminformatics'],
 [135, 'Computational  Biology'],
 [109, 'Computational Physics'],
 [20, 'Computer Engineering'],
 [110, 'Condensed Matter Physics'],
 [57, 'Cosmology'],
 [66, 'Crystallography'],
 [95, 'Design'],
 [61, 'Developmental Biology'],
 [39, 'Ecology'],
 [27, 'Economics'],
 [129, 'Education'],
 [117, 'Entropy'],
 [31, 'Environmental chemistry'],
 [34, 'Environmental science'],
 [24, 'Evolutionary biology'],
 [56, 'Galactic Astronomy'],
 [118, 'General Relativity'],
 [90, 'Genetic Engineering'],
 [13, 'Genetics'],
 [32, 'Geochemistry'],
 [17, 'Geography'],
 [29, 'Geology'],
 [103, 'Geometry'],
 [79, 'Geophysics'],
 [128, 'Hematology'],
 [126, 'History'],
 [80, 'Hydrology'],
 [46, 'Immunology'],
 [132, 'Infectious Diseases'],
 [69, 'Inorganic Chemistry'],
 [97, 'Law'],
 [35, 'Limnology'],
 [98, 'Literature'],
 [119, 'M-Theory'],
 [62, 'Marine Biology'],
 [91, 'Mechanical Engineering'],
 [111, 'Mechanics'],
 [7, 'Medicine'],
 [122, 'Mental Health'],
 [8, 'Microbiology'],
 [82, 'Mineralogy'],
 [70, 'Molecular Physics'],
 [14, 'Molecular biology'],
 [136, 'NMR Spectroscopy'],
 [15, 'Neuroscience'],
 [71, 'Nuclear Chemistry'],
 [92, 'Nuclear Engineering'],
 [138, 'Numerical Analysis'],
 [36, 'Oceanography'],
 [37, 'Organic chemistry'],
 [84, 'Paleoclimatology'],
 [28, 'Paleontology'],
 [85, 'Palynology'],
 [63, 'Parasitology'],
 [112, 'Particle Physics'],
 [139, 'Pathology'],
 [99, 'Performing Arts'],
 [19, 'Pharmacology'],
 [100, 'Philosophy'],
 [86, 'Physical Geography'],
 [16, 'Physiology'],
 [54, 'Planetary Geology'],
 [59, 'Planetary Science'],
 [133, 'Plant Biology'],
 [113, 'Plasma Physics'],
 [104, 'Probability'],
 [114, 'Quantum Mechanics'],
 [73, 'Radiochemistry'],
 [106, 'Science Policy'],
 [45, 'Sociology'],
 [23, 'Software Engineering'],
 [87, 'Soil Science'],
 [115, 'Solid Mechanics'],
 [120, 'Special Relativity'],
 [105, 'Statistics'],
 [55, 'Stellar Astronomy'],
 [47, 'Stereochemistry'],
 [75, 'Supramolecular Chemistry'],
 [130, 'Survey results'],
 [76, 'Theoretical Computer Science'],
 [116, 'Thermodynamics'],
 [44, 'Toxicology'],
 [134, 'Virology']];

function build_idea_list_item(idea) {
    if(idea.idea_text.length > 255) {
        idea.idea_text = idea.idea_text.substr(0, 252) + "...";
    }
    var html = '<a href="/ideas/'+idea.id+'" class="list-group-item">' +
      '<h4 class="list-group-item-heading">'+idea.title+'</h4>' +
      '<p class="cat">posted in <u>'+idea.category+'</u></p>' +
      '<p class="text list-group-item-text">'+idea.idea_text+'</p>' +
    '</a>';
    return html;
}

function search(query) {
    $("#search-result-container a").remove();
    $.get("/search", {"q": query}).success(function(data) {
        data = data.results;
        var target = $("#search-result-container");
        console.log("=============================");
        console.log(data);
        for(var i=0; i<data.length; i++) {
            console.log(data[i]);
            target.append(build_idea_list_item(data[i]));
        }
    });
}

$(document).ready(function() {
    //open idea form when "Upload an Idea" is clicked
    $("a#open_idea_form").click(function() {
        if(!LOGGED_IN) {
            alert("Please log in by using the 'Log in with Figshare' button.");
            return false;
        }
        $("form#idea_form").show();
        $("select").chosen();
        $("a#open_idea_form").hide();
        return false;
    });

    //word counter
    $("textarea#idea_text").keyup(function() {
        var obj = $(this);
        text = obj.val();
        if(text === "") {
            wordcount = 0;
        } else {
            wordcount = $.trim(text).split(" ").length;
        }
        $("#wordcount").html('' + wordcount);
    });

    //automatically build option list from "categories"
    var select = $("#category_select");
    for(var i=0; i < categories.length; i++) {
        select.append("<option value='"+categories[i][0]+"'>"+categories[i][1]+"</option>");
    }

    //search functionality
    var searchTimeout = null;
    $('input[name=query]').keyup(function() {
        clearTimeout(searchTimeout);
        var target = $(this);
        searchTimeout = setTimeout(function() { search(target.val()); }, 500);
    });
});
