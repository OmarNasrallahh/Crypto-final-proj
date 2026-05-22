<!-- =========================================================
     JAVASCRIPT
     ========================================================= -->
<script>

/* ----------------------------------------------------------
   TAB SWITCHING
   ---------------------------------------------------------- */
function switchTab(name) {
  // Hide all panels and deactivate all buttons
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

  // Show selected panel and activate matching button
  document.getElementById('tab-' + name).classList.add('active');
  // Find which button triggered this (by matching onclick text)
  event.target.classList.add('active');
}

/* ----------------------------------------------------------
   UTILITY – show status message
   ---------------------------------------------------------- */
function setStatus(id, msg, isOk) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.className = 'status ' + (isOk ? 'ok' : 'err');
}

/* ----------------------------------------------------------
   UTILITY – copy output text to clipboard
   ---------------------------------------------------------- */
function copyText(spanId) {
  const text = document.getElementById(spanId).textContent;
  navigator.clipboard.writeText(text).catch(() => {});
}

/* ==========================================================
   1. SYMMETRIC ENCRYPTION / DECRYPTION
   
   CryptoJS library documentation:
   https://cryptojs.gitbook.io/docs/

   How CryptoJS works here:
   - CryptoJS.AES.encrypt(message, key)  → returns a CipherParams object
   - .toString()                          → serializes to OpenSSL-compatible string
   - CryptoJS.AES.decrypt(ciphertext, key) → returns WordArray
   - .toString(CryptoJS.enc.Utf8)          → converts back to readable string

   Same pattern applies for DES and TripleDES.
   ========================================================== */

function symEncrypt() {
  const algo  = document.getElementById('sym-algo').value;   // e.g. "AES"
  const input = document.getElementById('sym-input').value.trim();
  const key   = document.getElementById('sym-key').value.trim();

  // Input validation
  if (!input || !key) {
    setStatus('sym-status', '⚠ Please fill in both plaintext and key.', false);
    return;
  }

  try {
    // CryptoJS[algo] accesses CryptoJS.AES / CryptoJS.DES / CryptoJS.TripleDES dynamically
    const encrypted = CryptoJS[algo].encrypt(input, key).toString();
    document.getElementById('sym-output-text').textContent = encrypted;
    setStatus('sym-status', `✓ Encrypted with ${algo} successfully.`, true);
  } catch(e) {
    setStatus('sym-status', '✗ Encryption failed: ' + e.message, false);
  }
}

function symDecrypt() {
  const algo  = document.getElementById('sym-algo').value;
  const input = document.getElementById('sym-input').value.trim();
  const key   = document.getElementById('sym-key').value.trim();

  if (!input || !key) {
    setStatus('sym-status', '⚠ Please fill in both ciphertext and key.', false);
    return;
  }

  try {
    // decrypt() returns a WordArray; convert to UTF-8 string
    const decrypted = CryptoJS[algo].decrypt(input, key).toString(CryptoJS.enc.Utf8);

    if (!decrypted) {
      setStatus('sym-status', '✗ Decryption failed: wrong key or corrupted ciphertext.', false);
      return;
    }

    document.getElementById('sym-output-text').textContent = decrypted;
    setStatus('sym-status', `✓ Decrypted with ${algo} successfully.`, true);
  } catch(e) {
    setStatus('sym-status', '✗ Decryption error: ' + e.message, false);
  }
}


/* ==========================================================
   2. RSA (ASYMMETRIC)

   We use the JSEncrypt library (wrapper around forge / JSBN).

   WORKFLOW:
   1. Generate key pair → store public + private PEM strings
   2. Encrypt:  create JSEncrypt instance → setPublicKey(pem) → encrypt(msg)
   3. Decrypt:  create JSEncrypt instance → setPrivateKey(pem) → decrypt(cipher)

   PEM format: -----BEGIN RSA PUBLIC KEY----- ... -----END RSA PUBLIC KEY-----
   Base64-encoded DER structure inside.

   LIMITATION: RSA can only encrypt data shorter than the key size minus padding.
   For 2048-bit key → max ~214 bytes of plaintext with PKCS#1 v1.5 padding.
   ========================================================== */

let rsaPublicKey  = '';   // stored so user can auto-fill encrypt tab
let rsaPrivateKey = '';

function generateRSAKeys() {
  setStatus('rsa-gen-status', '⏳ Generating 2048-bit key pair... (this may take a moment)', true);

  // Small timeout so the status message renders before blocking computation
  setTimeout(() => {
    try {
      const crypt = new JSEncrypt({ default_key_size: 2048 });
      crypt.getKey();  // triggers key generation

      rsaPublicKey  = crypt.getPublicKey();
      rsaPrivateKey = crypt.getPrivateKey();

      document.getElementById('rsa-pub').textContent  = rsaPublicKey;
      document.getElementById('rsa-priv').textContent = rsaPrivateKey;

      // Auto-populate the encrypt/decrypt forms for convenience
      document.getElementById('rsa-enc-pub').value  = rsaPublicKey;
      document.getElementById('rsa-dec-priv').value = rsaPrivateKey;

      setStatus('rsa-gen-status', '✓ 2048-bit RSA key pair generated.', true);
    } catch(e) {
      setStatus('rsa-gen-status', '✗ Key generation failed: ' + e.message, false);
    }
  }, 50);
}

function rsaEncrypt() {
  const msg    = document.getElementById('rsa-enc-input').value.trim();
  const pubKey = document.getElementById('rsa-enc-pub').value.trim();

  if (!msg || !pubKey) {
    setStatus('rsa-enc-status', '⚠ Provide both message and public key.', false);
    return;
  }

  try {
    const encrypt = new JSEncrypt();
    encrypt.setPublicKey(pubKey);
    const result = encrypt.encrypt(msg);  // returns Base64 ciphertext or false

    if (!result) {
      setStatus('rsa-enc-status', '✗ Encryption failed. Check your public key.', false);
      return;
    }

    document.getElementById('rsa-enc-out').textContent = result;
    setStatus('rsa-enc-status', '✓ Encrypted with RSA public key.', true);
  } catch(e) {
    setStatus('rsa-enc-status', '✗ Error: ' + e.message, false);
  }
}

function rsaDecrypt() {
  const cipher  = document.getElementById('rsa-dec-input').value.trim();
  const privKey = document.getElementById('rsa-dec-priv').value.trim();

  if (!cipher || !privKey) {
    setStatus('rsa-dec-status', '⚠ Provide both ciphertext and private key.', false);
    return;
  }

  try {
    const decrypt = new JSEncrypt();
    decrypt.setPrivateKey(privKey);
    const result = decrypt.decrypt(cipher);  // returns plaintext string or false

    if (!result) {
      setStatus('rsa-dec-status', '✗ Decryption failed. Check your private key.', false);
      return;
    }

    document.getElementById('rsa-dec-out').textContent = result;
    setStatus('rsa-dec-status', '✓ Decrypted with RSA private key.', true);
  } catch(e) {
    setStatus('rsa-dec-status', '✗ Error: ' + e.message, false);
  }
}


/* ==========================================================
   3. ENCODING / DECODING

   Base64:
     btoa(str)  – encode  (binary to ASCII)
     atob(str)  – decode  (ASCII to binary)
     
     IMPORTANT: btoa only handles Latin-1 characters. For Unicode
     text we use encodeURIComponent + escape trick.

   Hex:
     Each character has a Unicode code point (e.g. 'A' = 65 = 0x41).
     Encoding: map each char → charCode → hex string (padded to 2 digits).
     Decoding: split every 2 chars → parseInt(hex, 16) → char.

   URL:
     encodeURIComponent(str) – encodes all special chars except A-Z a-z 0-9 - _ . ! ~ * ' ( )
     decodeURIComponent(str) – reverses it.
     Space becomes %20, & becomes %26, etc.
   ========================================================== */

function encEncode() {
  const scheme = document.getElementById('enc-algo').value;
  const text   = document.getElementById('enc-input').value;

  if (!text) { setStatus('enc-status','⚠ Enter some text first.', false); return; }

  try {
    let result;
    if (scheme === 'base64') {
      // Unicode-safe Base64 encode
      result = btoa(unescape(encodeURIComponent(text)));
    } else if (scheme === 'hex') {
      // Convert each character to its 2-digit hex representation
      result = Array.from(text)
                 .map(c => c.charCodeAt(0).toString(16).padStart(2,'0'))
                 .join('');
    } else {  // url
      result = encodeURIComponent(text);
    }
    document.getElementById('enc-out').textContent = result;
    setStatus('enc-status', `✓ Encoded as ${scheme.toUpperCase()}.`, true);
  } catch(e) {
    setStatus('enc-status', '✗ Encode error: ' + e.message, false);
  }
}

function encDecode() {
  const scheme = document.getElementById('enc-algo').value;
  const text   = document.getElementById('enc-input').value.trim();

  if (!text) { setStatus('enc-status','⚠ Enter encoded text first.', false); return; }

  try {
    let result;
    if (scheme === 'base64') {
      // Unicode-safe Base64 decode
      result = decodeURIComponent(escape(atob(text)));
    } else if (scheme === 'hex') {
      // Split into pairs of hex digits, convert each to char
      if (text.length % 2 !== 0) throw new Error('Invalid hex string length.');
      result = text.match(/.{2}/g)
                   .map(h => String.fromCharCode(parseInt(h, 16)))
                   .join('');
    } else {  // url
      result = decodeURIComponent(text);
    }
    document.getElementById('enc-out').textContent = result;
    setStatus('enc-status', `✓ Decoded from ${scheme.toUpperCase()}.`, true);
  } catch(e) {
    setStatus('enc-status', '✗ Decode error: ' + e.message, false);
  }
}


/* ==========================================================
   4. HASHING

   SHA-256: produces a 256-bit (64 hex chars) digest.
   SHA-512: produces a 512-bit (128 hex chars) digest.
   
   Salted hashing:
     salt = random 16-byte value (here as hex string)
     stored_hash = SHA256(salt + password)
     To verify: re-hash (salt + input) and compare.
     WHY SALT? Without it, identical passwords produce identical hashes.
     An attacker with a pre-computed rainbow table can instantly crack them.
     A random salt makes each hash unique even for identical inputs.
   ========================================================== */

// Show/hide salt input based on selected algorithm
document.getElementById('hash-algo').addEventListener('change', function() {
  document.getElementById('salt-row').style.display =
    this.value === 'salted' ? 'block' : 'none';
  if (this.value === 'salted') genSalt();
});

// Generate a cryptographically random 16-byte salt as hex string
function genSalt() {
  const arr = new Uint8Array(16);
  window.crypto.getRandomValues(arr);  // Web Crypto API – truly random
  document.getElementById('hash-salt').value =
    Array.from(arr).map(b => b.toString(16).padStart(2,'0')).join('');
}

function computeHash() {
  const algo  = document.getElementById('hash-algo').value;
  const input = document.getElementById('hash-input').value;

  if (!input) { setStatus('hash-status','⚠ Enter text to hash.', false); return; }

  try {
    let result;

    if (algo === 'SHA256') {
      // CryptoJS.SHA256 returns a WordArray; .toString() gives lowercase hex
      result = CryptoJS.SHA256(input).toString();

    } else if (algo === 'SHA512') {
      result = CryptoJS.SHA512(input).toString();

    } else {
      // Salted SHA-256
      let salt = document.getElementById('hash-salt').value.trim();
      if (!salt) { genSalt(); salt = document.getElementById('hash-salt').value; }

      // Concatenate salt + input, then hash
      const salted = salt + input;
      const hash   = CryptoJS.SHA256(salted).toString();

      // Display both salt and hash so user can store/verify later
      result = `SALT:  ${salt}\nHASH:  ${hash}`;
    }

    document.getElementById('hash-out').textContent = result;
    setStatus('hash-status', `✓ Hash computed using ${algo}.`, true);
  } catch(e) {
    setStatus('hash-status', '✗ Hashing error: ' + e.message, false);
  }
}

</script>
</body>
</html>