// Supposons que vous ayez un bouton de suppression avec la classe 'deleteButton'
$('.deleteButton').click(function() {
    var contactId = $(this).data('contact-id');

    $.ajax({
        type: 'POST',
        url: '{% url "delete_contact" %}',  // Assurez-vous de mettre à jour l'URL
        data: {
            'contact_id': contactId,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function(response) {
            // Gérer la réponse après la suppression du contact
            console.log(response);
        },
        error: function(error) {
            // Gérer les erreurs
            console.log(error);
        }
    });
});

// Supposons que vous ayez un formulaire de mise à jour avec l'id 'updateForm'
$('#updateForm').submit(function(e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '{% url "update_contact" contact.id %}',  // Assurez-vous de mettre à jour l'URL
        data: $(this).serialize(),
        success: function(response) {
            // Gérer la réponse après la mise à jour du contact
            console.log(response);
        },
        error: function(error) {
            // Gérer les erreurs
            console.log(error);
        }
    });
});

// Supposons que vous ayez une liste avec l'id 'contactList'
$.ajax({
    type: 'GET',
    url: '{% url "get_contacts" %}',  // Assurez-vous de mettre à jour l'URL
    success: function(response) {
        // Gérer la réponse après la lecture des contacts
        console.log(response);

        // Mettez à jour la liste des contacts sur la page avec la réponse
        // Exemple: $('#contactList').html(response);
    },
    error: function(error) {
        // Gérer les erreurs
        console.log(error);
    }
});
 // Supposons que vous ayez un formulaire avec l'id 'contactForm'
$('#contactForm').submit(function(e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '{% url "create_contact" %}',  // Assurez-vous de mettre à jour l'URL
        data: $(this).serialize(),
        success: function(response) {
            // Gérer la réponse après la création du contact
            console.log(response);
        },
        error: function(error) {
            // Gérer les erreurs
            console.log(error);
        }
    });
});
