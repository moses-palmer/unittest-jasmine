describe("TestRunner", function() {
    it("spec 1", function() {
        expect(1).toEqual(1);
        function func() {
            expect(2).toEqual(1);
        }
        func();
    });

    describe("inner suite", function() {
        it("inner spec 1", function() {
            expect(1).toEqual(1);
        });

        it("inner spec 2", function() {
            expect(1).toEqual(2);
        });
    });

    it("spec 2", function() {
        expect(1).toEqual(1);
    });
});
