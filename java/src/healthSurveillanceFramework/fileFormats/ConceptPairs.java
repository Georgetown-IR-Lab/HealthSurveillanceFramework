package healthSurveillanceFramework.fileFormats;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ConceptPairs extends JsonFile {
    private Map<String, List<String>> conceptPairs;

    @SuppressWarnings("unchecked")
    public void loadJson(String filename) {
        String json = readFile(filename);
        conceptPairs = parser.parseJson(json);
    }

    public void writeJson(String filename) {
         String json = generator.generateJson(conceptPairs);

        // quick-json encloses the data in an outside array
        // TODO figure out a better way to handle this
        json = json.substring(1, json.length() - 1);

        writeFile(json, filename);
    }

    public Map<String, List<String>> getConceptPairs() {
        return conceptPairs;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("usage: <ConceptPairs file>");
            System.exit(1);
        }

        ConceptPairs cp = new ConceptPairs();
        cp.loadJson(args[0]);

        System.out.println("ConceptPairs found in '" + args[0] + "':");
        for (String concept : cp.getConceptPairs().keySet())
            for (String docid : cp.getConceptPairs().get(concept))
                System.out.println("\t" + concept + "\t" + docid);
    }

}
