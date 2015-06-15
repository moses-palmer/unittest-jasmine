describe("Jasmine loader", function() {
    it("runs a successful test", function() {
        expect(1).toEqual(1);
    });

    function thrower() {
        throw "Failure";
    }

    function nothrower() {
    }

    it("throws successfully", function() {
        expect(thrower).toThrow();
    });

    it("throws nothing", function() {
       expect(nothrower).not.toThrow();
    });

    it("does not throw and fails (SHOULD FAIL)", function() {
       expect(nothrower).toThrow();
    });
});
