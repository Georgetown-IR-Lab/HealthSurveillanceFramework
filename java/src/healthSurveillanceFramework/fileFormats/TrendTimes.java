package healthSurveillanceFramework.fileFormats;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class TrendTimes extends JsonFile {
    private Map<String, List<Map<String, String>>> trendTimes;

    @SuppressWarnings("unchecked")
    public void loadJson(String filename) {
        String json = readFile(filename);
        trendTimes = parser.parseJson(json);
    }

    public void writeJson(String filename) {
         String json = generator.generateJson(trendTimes);

        // quick-json encloses the data in an outside array
        // TODO figure out a better way to handle this
        json = json.substring(1, json.length() - 1);

        writeFile(json, filename);
    }

    public Map<String, List<Map<String, String>>> getTrendTimes() {
        return trendTimes;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("usage: <TrendTimes file>");
            System.exit(1);
        }

        TrendTimes t = new TrendTimes();
        t.loadJson(args[0]);

        System.out.println("TrendTimes found in '" + args[0] + "':");
        for (String concept : t.getTrendTimes().keySet())
            for (Map times : t.getTrendTimes().get(concept))
                System.out.println("\t" + concept + "\t" + times);
    }

}
