import { newE2EPage } from '@stencil/core/testing';

describe('lwc-limepkg-scrive', () => {
    let page;
    beforeEach(async () => {
        page = await newE2EPage();
    });

    describe('render', () => {
        let button;
        beforeEach(async () => {
            await page.setContent(`
                <lwc-limepkg-scrive></lwc-limepkg-scrive>
            `);
            await page.find('lwc-limepkg-scrive');

            // `>>>` means that `limel-button` is inside the
            // shadow-DOM of `lwc-limepkg-scrive`
            button = await page.find(`
                lwc-limepkg-scrive >>> limel-button
            `);
        });
        it('displays the correct label', () => {
            expect(button).toEqualAttribute('label', 'Hello World!');
        });
    });
});
