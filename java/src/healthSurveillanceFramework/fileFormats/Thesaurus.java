package healthSurveillanceFramework.fileFormats;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Thesaurus extends JsonFile {
    private Map<String, Set<String>> thesaurus;

    @SuppressWarnings("unchecked")
    public void loadJson(String filename) {
        String json = readFile(filename);
        Map<String, ArrayList<String>> data = (Map<String, ArrayList<String>>) parser.parseJson(json);

        thesaurus = new HashMap<String, Set<String>>();
        for (String entryid : data.keySet()) {
            thesaurus.put(entryid, new HashSet(data.get(entryid)));
        }
    }

    public void writeJson(String filename) {
         String json = generator.generateJson(thesaurus);

        // quick-json encloses the data in an outside array
        // TODO figure out a better way to handle this
        json = json.substring(1, json.length() - 1);

        writeFile(json, filename);
    }

    public Map<String, Set<String>> getThesaurus() {
        return thesaurus;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("usage: <Thesaurus file>");
            System.exit(1);
        }

        Thesaurus t = new Thesaurus();
        t.loadJson(args[0]);

        System.out.println("thesaurus entry ids found in '" + args[0] + "':");
        for (String entryid : t.getThesaurus().keySet())
            System.out.println("\t" + entryid);
    }

}
