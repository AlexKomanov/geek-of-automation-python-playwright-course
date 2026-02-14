from playwright.sync_api import expect, Page

def test_example(page: Page):
    page.goto('https://www.saucedemo.com/')
    page.get_by_placeholder('Username').fill('standard_user')
    page.locator('[name="password"]').press_sequentially('secret_sauce', delay=300)
    page.get_by_role('button', name='Login').click()
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html', timeout=10000)
    expect(page.locator('[data-test="secondary-header"]')).to_match_aria_snapshot("""
    - text: Products Name (A to Z)
    - combobox:
      - option "Name (A to Z)" [selected]
      - option "Name (Z to A)"
      - option "Price (low to high)"
      - option "Price (high to low)"
    """)






