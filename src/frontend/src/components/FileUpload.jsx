import { useState, useRef } from 'react'
import axios from 'axios'

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
        } catch (error) {
            console.error("Upload failed", error)
            alert("Erro no upload")
        } finally {
            setUploading(false)
        }
    }

    return (
        <div
            className="upload-zone"
            style={{
                border: `2px dashed ${isDragOver ? '#3b82f6' : 'rgba(255,255,255,0.2)'}`,
                borderRadius: '12px',
                padding: '3rem',
                textAlign: 'center',
                cursor: 'pointer',
                background: isDragOver ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
                transition: 'all 0.2s'
            }}
            onDragOver={(e) => { e.preventDefault(); setIsDragOver(true) }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={(e) => {
                e.preventDefault()
                setIsDragOver(false)
                handleFile(e.dataTransfer.files[0])
            }}
            onClick={() => fileInputRef.current.click()}
        >
            <input
                type="file"
                hidden
                ref={fileInputRef}
                onChange={(e) => handleFile(e.target.files[0])}
            />
            {uploading ? (
                <p>Processando inteligência artificial...</p>
            ) : (
                <div>
                    <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Clique ou arraste um documento</p>
                    <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Suporta JPG, PNG, PDF</p>
                </div>
            )}
        </div>
    )
}
