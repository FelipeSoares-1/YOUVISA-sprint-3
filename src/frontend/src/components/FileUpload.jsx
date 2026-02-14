import { useState, useRef } from 'react'
import axios from 'axios'

// SVG Icons
const UploadCloudIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--accent-light)', marginBottom: '0.5rem' }}>
        <polyline points="16 16 12 12 8 16" />
        <line x1="12" y1="12" x2="12" y2="21" />
        <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" />
    </svg>
)

const SpinnerIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
        style={{ animation: 'spin 1s linear infinite', color: 'var(--accent-light)' }}>
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
        <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
    </svg>
)

export default function FileUpload({ onUploadSuccess }) {
    const [isDragOver, setIsDragOver] = useState(false)
    const [uploading, setUploading] = useState(false)
    const fileInputRef = useRef(null)

    const handleFile = async (file) => {
        if (!file) return
        setUploading(true)

        const formData = new FormData()
        formData.append('file', file)

        try {
            const response = await axios.post('http://localhost:8000/api/documents/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })
            onUploadSuccess(response.data)
        } catch {
            alert("Erro no upload. Tente novamente.")
        } finally {
            setUploading(false)
        }
    }

    return (
        <div
            className="upload-zone"
            style={{
                borderColor: isDragOver ? 'var(--accent) !important' : undefined,
                background: isDragOver ? 'rgba(99, 102, 241, 0.08) !important' : undefined,
            }}
            onDragOver={(e) => { e.preventDefault(); setIsDragOver(true) }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={(e) => {
                e.preventDefault()
                setIsDragOver(false)
                handleFile(e.dataTransfer.files[0])
            }}
            onClick={() => fileInputRef.current.click()}
            role="button"
            tabIndex={0}
            aria-label="Área de upload de documentos"
        >
            <input
                type="file"
                hidden
                ref={fileInputRef}
                onChange={(e) => handleFile(e.target.files[0])}
                accept=".jpg,.jpeg,.png,.pdf,.txt"
            />
            {uploading ? (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
                    <SpinnerIcon />
                    <p style={{ color: 'var(--accent-light)', fontSize: '0.9rem' }}>Processando com IA...</p>
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative', zIndex: 1 }}>
                    <UploadCloudIcon />
                    <p style={{ fontSize: '1rem', fontWeight: 500, fontFamily: 'var(--font-display)', marginBottom: '0.25rem' }}>
                        Clique ou arraste um documento
                    </p>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>
                        Suporta JPG, PNG, PDF, TXT
                    </p>
                </div>
            )}
        </div>
    )
}
