# 🔐 Set Up SSH Key for GitHub

Follow these steps to generate and configure an SSH key for authenticating with GitHub.

---

## 1. Generate an SSH Key

Run the following command to create a new SSH key using the Ed25519 algorithm (recommended by GitHub):

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

> Replace `your_email@example.com` with the email associated with your GitHub account.

---

## 2. Enter a Passphrase (Optional)

When prompted:

- You **can** type a passphrase for added security (you’ll need to enter it each time you push/pull).
- Or, just press **Enter twice** to skip and leave it empty (not recommended for production use).

---

## 3. Start the SSH Agent

Start the agent in your shell:

```bash
eval "$(ssh-agent -s)"
# Example output: Agent pid 59566
```

---

## 4. Add Your Private Key to the Agent

```bash
ssh-add ~/.ssh/id_ed25519
```

---

## 5. Add Your Public Key to GitHub

1. Copy your public key to the clipboard:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. Go to [GitHub SSH keys settings](https://github.com/settings/keys).
3. Click **“New SSH key”**.
4. Give your key a meaningful **Title** (e.g., *Work Laptop*).
5. Paste the copied key into the **Key** field.
6. Click **Add SSH key**.

---

## 🔗 Useful References

- [Generate a new SSH key and add it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Add an SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)