document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const generateBtn = document.getElementById('generate-btn');
    const loadingDiv = document.getElementById('loading');
    const resultSection = document.getElementById('result-section');
    const summaryText = document.getElementById('summary-text');
    const copyBtn = document.getElementById('copy-btn');
    const downloadBtn = document.getElementById('download-btn');

    let selectedFile = null;

    // Drag & Drop Handling
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (file.type !== 'application/pdf') {
            alert('Veuillez sélectionner un fichier PDF.');
            return;
        }
        selectedFile = file;
        fileNameDisplay.textContent = file.name;
        generateBtn.disabled = false;
        
        // Reset UI
        resultSection.classList.add('hidden');
    }

    // Generate Summary
    generateBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const summaryType = document.querySelector('input[name="summary_type"]:checked').value;
        const chunkSize = document.getElementById('chunk_size').value;

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('summary_type', summaryType);
        formData.append('chunk_size', chunkSize);

        // UI Updates
        generateBtn.disabled = true;
        loadingDiv.classList.remove('hidden');
        resultSection.classList.add('hidden');
        summaryText.textContent = '';

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                summaryText.textContent = data.summary;
                resultSection.classList.remove('hidden');
                
                // Scroll to result
                resultSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Erreur: ' + (data.error || 'Une erreur est survenue'));
            }
        } catch (error) {
            alert('Erreur de connexion: ' + error.message);
        } finally {
            loadingDiv.classList.add('hidden');
            generateBtn.disabled = false;
        }
    });

    // Copy to Clipboard
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(summaryText.textContent).then(() => {
            const originalIcon = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                copyBtn.innerHTML = originalIcon;
            }, 2000);
        });
    });

    // Download Summary
    downloadBtn.addEventListener('click', () => {
        const text = summaryText.textContent;
        const blob = new Blob([text], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `resume_${selectedFile.name.replace('.pdf', '')}.txt`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    });
});
