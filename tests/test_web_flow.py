from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:5000"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        assert "Biblioteca Virtual" in page.text_content("body")

        page.fill("#titulo", "Dom Casmurro")
        page.click("text=Buscar por nome")
        page.wait_for_load_state("networkidle")
        assert "Dom Casmurro" in page.text_content("body")

        page.click("text=Ver detalhes")
        page.wait_for_load_state("networkidle")
        body = page.text_content("body")
        assert "ISBN" in body
        assert "Você também pode gostar" in body

        page.goto(BASE_URL)
        page.fill("#isbn", "9780720608458")
        page.click("text=Buscar por ISBN")
        page.wait_for_load_state("networkidle")
        assert "Dom Casmurro" in page.text_content("body")

        page.goto(BASE_URL)
        page.fill("#isbn", "0000000000000")
        page.click("text=Buscar por ISBN")
        page.wait_for_load_state("networkidle")
        assert "Livro não encontrado." in page.text_content("body")

        browser.close()


if __name__ == "__main__":
    main()
