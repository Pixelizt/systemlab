import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import mermaid from 'mermaid';
import { useParams } from 'react-router-dom';

mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    fontFamily: 'system-ui, sans-serif',
    primaryColor: '#000000',
    primaryTextColor: '#ffffff',
    primaryBorderColor: '#333333',
    lineColor: '#999999',
    secondaryColor: '#fafafa'
  }
});

function MermaidChart({ chart }: { chart: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current && chart) {
      mermaid.render(`mermaid-${Math.random().toString(36).substr(2, 9)}`, chart).then(result => {
        if (ref.current) ref.current.innerHTML = result.svg;
      }).catch(e => console.error('Mermaid render error', e));
    }
  }, [chart]);

  return <div ref={ref} className="mermaid-container" />;
}

export default function SopRenderer() {
  const { categoryId, sopId } = useParams();
  const [content, setContent] = useState('# Loading...');

  useEffect(() => {
    // In a real app, this would fetch from an API or dynamic import.
    // For MVP, we simulate fetching content based on the URL.
    if (!categoryId || !sopId) return;
    
    // Simulate content
    const demoContent = `
# Demo SOP: ${sopId.replace(/-/g, ' ')}
*Category: ${categoryId}*

This is a demonstration of the SystemLab standard operating procedure format.

## Flowchart
\`\`\`mermaid
graph TD
  A[Start Process] --> B{Is it qualified?};
  B -- Yes --> C[Proceed to next step];
  B -- No --> D[End process];
\`\`\`

## Video Walkthrough
\`\`\`loom
https://www.loom.com/share/example-id
\`\`\`

## Text Instructions
1. Follow the flowchart above.
2. Ensure you have reviewed the video.
3. Mark complete in your tracking tool.
    `;
    
    setContent(demoContent);
  }, [categoryId, sopId]);

  return (
    <div className="sop-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code({node, inline, className, children, ...props}: any) {
            const match = /language-(\w+)/.exec(className || '');
            const lang = match ? match[1] : '';
            
            if (!inline && lang === 'mermaid') {
              return <MermaidChart chart={String(children).replace(/\n$/, '')} />;
            }
            if (!inline && lang === 'loom') {
              const url = String(children).trim();
              const id = url.split('/').pop();
              return (
                <div className="loom-container">
                  <iframe 
                    src={`https://www.loom.com/embed/${id}`} 
                    frameBorder="0" 
                    allowFullScreen 
                    style={{width: '100%', height: '400px', borderRadius: '8px', border: '1px solid #eaeaea'}}>
                  </iframe>
                </div>
              );
            }
            return <code className={className} {...props}>{children}</code>;
          }
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
