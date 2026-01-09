document$.subscribe(function() {
  const headers = document.querySelectorAll("article h1, article h2, article h3");

  headers.forEach(header => {
    if (header.querySelector(".share-button")) return;

    const shareBtn = document.createElement("button");
    shareBtn.classList.add("share-button"); 
    shareBtn.setAttribute("title", "Share this section");
    shareBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81a3 3 0 0 0 3-3 3 3 0 0 0-3-3 3 3 0 0 0-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9a3 3 0 0 0-3 3 3 3 0 0 0 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.15c-.05.21-.08.43-.08.66 0 1.61 1.31 2.91 2.92 2.91s2.92-1.3 2.92-2.91a2.92 2.92 0 0 0-2.92-2.91"/></svg>';

    shareBtn.onclick = async (e) => {
      e.stopPropagation();
      e.preventDefault();
      
      // 1. Clean Title
      const tempClone = header.cloneNode(true);
      tempClone.querySelectorAll('.share-button, .headerlink').forEach(n => n.remove());
      const cleanTitle = tempClone.innerText.trim();

      // 2. Metadata
      const metaSiteName = document.querySelector('meta[property="og:site_name"]')?.content || "Okinawa is designed to fail";
      const metaAuthor = document.querySelector('meta[name="author"]')?.content || "りしき";
      
      // 3. URL
      const shareUrl = window.location.origin + window.location.pathname + (header.id ? "#" + header.id : "");

      // 4. THE FIX: Combine everything into one block
      // Apps can't ignore the URL if it's part of the text.
      const fullShareText = `"${cleanTitle}"\nvia ${metaSiteName} (by ${metaAuthor})\n${shareUrl}`;

      // 5. Share Logic
      if (navigator.share) {
        try {
          await navigator.share({
            title: cleanTitle, // System dialog title only
            text: fullShareText, // <-- We pass the URL here inside the text
            // url: shareUrl // <-- Removed to prevent duplication/conflict on some OS
          });
        } catch (err) {
          // If user cancels, do nothing.
        }
      } else {
        navigator.clipboard.writeText(fullShareText);
        alert("Link copied to clipboard!");
      }
    };

    header.prepend(shareBtn);
  });
});
