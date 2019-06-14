package cn.leancloud.play.plugin.getting_started;

import cn.leancloud.play.plugin.BoundRoom;
import cn.leancloud.play.plugin.DoNothingPlugin;
import cn.leancloud.play.plugin.Plugin;
import cn.leancloud.play.plugin.PluginFactory;
import cn.leancloud.play.utils.Log;

import java.util.Map;

public class MyFancyPluginFactory implements PluginFactory {
    @Override
    public Plugin create(BoundRoom room, String pluginName, Map<String, Object> initConfigs) {
        if (pluginName != null && pluginName.length() > 0) {
            switch (pluginName) {
                case "fancy-plugin":
                    return new MyFancyPlugin(room, initConfigs);
                case "master is watching you plugin":
                    return new MasterIsWatchingYouPlugin(room);
            }
        }

        Log.info("unknown plugin name {}, use DoNothingPlugin instead", pluginName);
        return new DoNothingPlugin(room);
    }
}
