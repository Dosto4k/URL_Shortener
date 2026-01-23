document.addEventListener('DOMContentLoaded', function() {
    const customNameInput = document.getElementById('id_code');
    const blockWithpreviewField = document.getElementById('block-field-preview')
    const previewField = document.getElementById('preview-field');

    function toggleGeneratedField() {
        if (customNameInput.value.trim() !== '') {
            blockWithpreviewField.style.display = 'block';
            previewField.value = 'http://127.0.0.1:8000/u/' + customNameInput.value;
        } else {
            blockWithpreviewField.style.display = 'none';
            previewField.value = '';
        }
    }

    customNameInput.addEventListener('input', toggleGeneratedField);

    toggleGeneratedField();
});
