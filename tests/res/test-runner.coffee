describe "TestRunner", ->
    it "spec 1", ->
        expect(1).toEqual(1)
        expect(2).toEqual(1)

    describe "inner suite", ->
        it "inner spec 1", ->
            expect(1).toEqual(1)

        it "inner spec 2", ->
            expect(1).toEqual(2)

    it "spec 2", ->
        expect(1).toEqual(1)
