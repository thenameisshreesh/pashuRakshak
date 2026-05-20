import React from 'react'
import { getFileUrl } from '../../api/files'

export default function FilePreview({ fileId, fileName, contentType }) {
  if (!fileId) return <div className="no-file">No file uploaded</div>

  const url = getFileUrl(fileId)
  const isImage = contentType?.startsWith('image/') || fileName?.match(/\.(jpg|jpeg|png|webp)$/i)
  const isPdf = contentType === 'application/pdf' || fileName?.endsWith('.pdf')
  const isVideo = contentType?.startsWith('video/') || fileName?.match(/\.(mp4|mpeg|mov)$/i)

  return (
    <div className="file-preview">
      {isImage ? (
        <div className="preview-image-container">
          <img src={url} alt={fileName || 'Uploaded file'} className="preview-image" />
          <a href={url} target="_blank" rel="noreferrer" className="preview-link">Open original</a>
        </div>
      ) : isPdf ? (
        <div className="preview-pdf-container">
          <span className="pdf-icon">📄</span>
          <span className="pdf-name">{fileName || 'Document.pdf'}</span>
          <a href={url} target="_blank" rel="noreferrer" className="preview-btn">View PDF</a>
        </div>
      ) : isVideo ? (
        <div className="preview-video-container">
          <video src={url} controls className="preview-video" />
          <a href={url} target="_blank" rel="noreferrer" className="preview-link">Open video</a>
        </div>
      ) : (
        <div className="preview-generic-container">
          <span className="file-icon">📎</span>
          <span className="file-name">{fileName || 'File'}</span>
          <a href={url} download className="preview-btn">Download</a>
        </div>
      )}
    </div>
  )
}
